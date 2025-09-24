import os
import random
import io
import csv
from datetime import datetime
from typing import Optional, List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from sqlmodel import SQLModel, Field, create_engine, select, Session as SQLModelSession
from sqlalchemy.orm import Session as AlchSession
from sqlalchemy import delete

# local/project imports
from services.analysis import find_idle_recommendations
import schemas
import crud
from db import SessionLocal as AlchSessionLocal, init_db as init_usage_db
from models import UsageRecord  # SQLAlchemy model used by usage endpoints

# ---------------- App ----------------
app = FastAPI(title="Cloud Cost Optimizer - Unified Backend")

# CORS: configurable via env var (comma-separated), fallback to localhost dev ports
_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
CORS_ORIGINS = [u.strip() for u in _origins.split(",") if u.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- SQLModel demo models ----------------
class Instance(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    cpu: int
    status: str
    cost: int


class ActionLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    instance_id: int
    action: str
    old_cpu: Optional[int] = None
    old_status: Optional[str] = None
    new_cpu: Optional[int] = None
    new_status: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    actor: Optional[str] = None


# ---------------- DB engine (SQLModel demo DB) ----------------
SQLITE_URL = os.getenv("SQLMODEL_DATABASE_URL", "sqlite:///./cloudopt.db")
if SQLITE_URL.startswith("sqlite"):
    engine = create_engine(SQLITE_URL, echo=False, connect_args={"check_same_thread": False})
else:
    engine = create_engine(SQLITE_URL, echo=False)


def init_db_and_seed():
    """
    Create demo tables and reset demo data on startup.
    Uses SQLModel's metadata and SQLAlchemy's delete to clear tables safely.
    """
    SQLModel.metadata.create_all(engine)
    with SQLModelSession(engine) as session:
        # clear demo tables (safe)
        session.exec(delete(ActionLog))
        session.exec(delete(Instance))
        session.commit()

        seed = [
            Instance(name="dev-server", cpu=3, status="running", cost=25),
            Instance(name="test-server", cpu=0, status="idle", cost=15),
            Instance(name="burst-server", cpu=65, status="running", cost=60),
        ]
        session.add_all(seed)
        session.commit()


# ---------------- Startup ----------------
@app.on_event("startup")
def on_startup():
    # demo DB: create + seed
    init_db_and_seed()
    # usage DB (SQLAlchemy): initialize (db creation/migrations handled by init_usage_db)
    init_usage_db()


# ---------------- Helpers ----------------
def log_action(session: SQLModelSession, instance_id: int, action: str, old_cpu, old_status, new_cpu, new_status, actor="demo-user"):
    log = ActionLog(
        instance_id=instance_id,
        action=action,
        old_cpu=old_cpu,
        old_status=old_status,
        new_cpu=new_cpu,
        new_status=new_status,
        actor=actor,
    )
    session.add(log)
    session.commit()


# ---------------- Basic health / root ----------------
@app.get("/")
def root():
    # <-- your requested snippet (now present)
    return {"message": "Backend running on Render 🚀"}


@app.get("/health")
def health():
    return {"status": "ok"}


# ---------------- SQLModel demo endpoints ----------------
@app.get("/instances", response_model=List[Instance])
def list_instances():
    with SQLModelSession(engine) as session:
        return session.exec(select(Instance)).all()


@app.get("/recommendations")
def recommendations():
    recs = []
    with SQLModelSession(engine) as session:
        insts = session.exec(select(Instance)).all()
        for inst in insts:
            if inst.cpu < 5 and inst.status in ("idle", "running"):
                recs.append({
                    "instance_id": inst.id,
                    "name": inst.name,
                    "recommendation": "Shutdown idle server",
                    "saving": inst.cost
                })
    return recs


@app.post("/make_idle/{instance_id}")
def make_idle(instance_id: int, actor: Optional[str] = None):
    with SQLModelSession(engine) as session:
        inst = session.get(Instance, instance_id)
        if not inst:
            raise HTTPException(status_code=404, detail="instance not found")
        old_cpu, old_status = inst.cpu, inst.status
        inst.cpu = 0
        inst.status = "idle"
        session.add(inst)
        session.commit()
        log_action(session, inst.id, "make_idle", old_cpu, old_status, inst.cpu, inst.status, actor or "demo-user")
        return {"updated": inst}


@app.post("/make_busy/{instance_id}")
def make_busy(instance_id: int, actor: Optional[str] = None):
    with SQLModelSession(engine) as session:
        inst = session.get(Instance, instance_id)
        if not inst:
            raise HTTPException(status_code=404, detail="instance not found")
        old_cpu, old_status = inst.cpu, inst.status
        inst.cpu = random.randint(20, 90)
        inst.status = "running"
        session.add(inst)
        session.commit()
        log_action(session, inst.id, "make_busy", old_cpu, old_status, inst.cpu, inst.status, actor or "demo-user")
        return {"updated": inst}


@app.get("/audit")
def get_audit(limit: int = 50):
    with SQLModelSession(engine) as session:
        rows = session.exec(select(ActionLog).order_by(ActionLog.timestamp.desc()).limit(limit)).all()
        return rows


# ---------------- CSV export endpoints ----------------
@app.get("/export/recommendations")
def export_recommendations_csv():
    recs = recommendations()
    stream = io.StringIO()
    writer = csv.writer(stream)
    writer.writerow(["instance_id", "name", "recommendation", "saving"])
    for r in recs:
        writer.writerow([r["instance_id"], r["name"], r["recommendation"], r["saving"]])
    stream.seek(0)
    headers = {"Content-Disposition": "attachment; filename=recommendations.csv"}
    return StreamingResponse(stream, media_type="text/csv", headers=headers)


@app.get("/export/audit")
def export_audit_csv(limit: int = 100):
    with SQLModelSession(engine) as session:
        rows = session.exec(
            select(ActionLog).order_by(ActionLog.timestamp.desc()).limit(limit)
        ).all()

        stream = io.StringIO()
        writer = csv.writer(stream)
        writer.writerow([
            "id", "instance_id", "action", "old_cpu", "old_status",
            "new_cpu", "new_status", "timestamp", "actor"
        ])
        for r in rows:
            writer.writerow([
                r.id, r.instance_id, r.action,
                r.old_cpu, r.old_status,
                r.new_cpu, r.new_status,
                r.timestamp, r.actor
            ])
        stream.seek(0)
        headers = {"Content-Disposition": "attachment; filename=audit_log.csv"}
        return StreamingResponse(stream, media_type="text/csv", headers=headers)


# ---------------- SQLAlchemy (Usage) endpoints ----------------
def get_usage_db():
    db = AlchSessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/usage", response_model=schemas.UsageOut)
def add_usage(usage: schemas.UsageCreate, db: AlchSession = Depends(get_usage_db)):
    """
    Add a usage record into the separate usage DB (cloud_costs.db).
    Uses the SQLAlchemy CRUD helper (crud.create_usage).
    """
    return crud.create_usage(db, usage)


@app.get("/usages", response_model=List[schemas.UsageOut])
def list_usages(db: AlchSession = Depends(get_usage_db)):
    """
    List all usage records from the usage DB.
    """
    return db.query(UsageRecord).all()


@app.get("/analysis/idle_recommendations")
def idle_recommendations(db: AlchSession = Depends(get_usage_db)):
    """
    Call the idle-recommendation logic from services/analysis.py
    """
    return find_idle_recommendations(db)


# ---------------- Local runner ----------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        log_level="info"
    )
