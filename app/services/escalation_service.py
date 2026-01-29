from app.extensions import db
from app.models import EscalationLog

def escalate_complaint(complaint, reason="High priority complaint"):
    escalation = EscalationLog(
        complaint_id=complaint.id,
        from_level="system",
        to_level="admin",
        reason=reason
    )

    db.session.add(escalation)
