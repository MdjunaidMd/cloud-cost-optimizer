# Cloud Cost Optimizer

**One-liner:** FastAPI backend + React frontend monorepo to simulate, analyze and optimize cloud resource costs. Designed for quick local setup, Docker-based dev, and painless deployment on Render.

---

# What’s in this repo : 

cloud-cost-optimizer/
├── backend/ # FastAPI app (main entry: backend/main.py)
├── frontend/ # React (Vite) dashboard
├── docker-compose.yml
├── requirements.txt # Backend Python deps
├── render.yaml # (optional) Render blueprint for auto-deploy
└── README.md

# Prerequisites (install first)

- Python 3.11 (or 3.10+)
- Node.js & npm (Node 18+ recommended)
- Git
- (Optional) Docker & Docker Compose — for full-stack local via containers

---

# Quick local setup — developer (Windows & macOS/Linux)

> These commands assume you are at the project root (`cloud-cost-optimizer`).

Clone (if not already)

git clone https://github.com/MdjunaidMd/cloud-cost-optimizer.git

cd cloud-cost-optimizer


# Create .env (IMPORTANT — do not commit)

Create a file .env at project root or in backend.

SQLModel demo DB (local SQLite) - ok for dev only
SQLMODEL_DATABASE_URL=sqlite:///./cloudopt.db

 Usage DB (SQLAlchemy) - local SQLite for dev
 DATABASE_URL=sqlite:///./cloud_costs.db

 App secrets & CORS
 SECRET_KEY=change_this_to_a_secure_value
 CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

  Frontend -> API base
  VITE_API_URL=http://127.0.0.1:8000


# Backend — run locally (Python venv)

# Windows (PowerShell):

cd C:\path\to\cloud-cost-optimizer

python -m venv .venv

.\.venv\Scripts\Activate

pip install -r requirements.txt

run API from project root:
uvicorn backend.main:

app --reload --host 127.0.0.1 --port 8000





# macOS / Linux (bash):

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000


# Verify:

Open: http://127.0.0.1:8000/ (root)

Health: http://127.0.0.1:8000/health

Demo endpoints: http://127.0.0.1:8000/instances, http://127.0.0.1:8000/recommendations



# Frontend — run locally (Vite)
cd frontend

npm install

npm run dev


Open http://127.0.0.1:5173 and confirm the dashboard loads.


# Full-stack via Docker

docker-compose up --build












