# backend/services/analysis.py

from models import UsageRecord

def find_idle_recommendations(db):
    """
    Look at usage records and recommend shutting down idle instances.
    For now, 'idle' = avg_cpu < 5
    """
    recs = []
    records = db.query(UsageRecord).all()

    for r in records:
        if r.cpu < 5:  # adjust logic as needed
            recs.append({
                "instance_id": r.id,
                "name": r.instance_name if hasattr(r, "instance_name") else "unknown",
                "recommendation": "Shutdown idle server",
                "saving": r.cost if hasattr(r, "cost") else 0,
            })

    return recs
