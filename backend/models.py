# backend/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from db import Base

class UsageRecord(Base):
    __tablename__ = "usage_records"

    id = Column(Integer, primary_key=True, index=True)
    cloud_provider = Column(String, index=True)   # e.g., AWS, GCP, Azure
    service_name = Column(String, index=True)     # e.g., EC2, S3
    resource_id = Column(String, index=True)      # resource identifier
    usage_amount = Column(Float)                  # hours, GB, etc.
    cost = Column(Float)                          # cost in $
    timestamp = Column(DateTime, default=datetime.utcnow)
