# backend/crud.py
from sqlalchemy.orm import Session
from backend import models, schemas   # ✅ fixed imports

def create_usage(db: Session, usage: schemas.UsageCreate):
    obj = models.UsageRecord(
        cloud_provider=usage.cloud_provider,
        service_name=usage.service_name,
        resource_id=usage.resource_id,
        usage_amount=usage.usage_amount,
        cost=usage.cost
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
