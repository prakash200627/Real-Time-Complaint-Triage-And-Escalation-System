from .extensions import db
from datetime import datetime, timezone


def utcnow_naive() -> datetime:
    # Python 3.13 deprecates datetime.utcnow(); keep DB timestamps as naive UTC
    return datetime.now(timezone.utc).replace(tzinfo=None)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200))
    role = db.Column(db.String(20), default="user")  

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    priority = db.Column(db.String(20))
    confidence = db.Column(db.Float)
    status = db.Column(db.String(20), default="open")
    created_at = db.Column(db.DateTime, default=utcnow_naive)

class EscalationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey("complaint.id"))
    from_level = db.Column(db.String(50))
    to_level = db.Column(db.String(50))
    reason = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=utcnow_naive)
