from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models import Complaint, EscalationLog
from app.services.status_service import is_valid_transition
from app.services.auth_service import get_current_user, user_has_role


admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@admin_bp.route("/escalations", methods=["GET"])
@jwt_required()
def view_escalations():
    user = get_current_user()
    if not user_has_role(user, "admin", "agent"):
        return {"msg": "Access denied"}, 403

    escalations = EscalationLog.query.all()
    return jsonify([
        {
            "id": e.id,
            "complaint_id": e.complaint_id,
            "from": e.from_level,
            "to": e.to_level,
            "reason": e.reason,
            "timestamp": e.timestamp.isoformat()
        } for e in escalations
    ])

@admin_bp.route("/complaints/<int:complaint_id>/status", methods=["PUT"])
@jwt_required()
def update_complaint_status(complaint_id):
    user = get_current_user()
    if not user_has_role(user, "admin", "agent"):
        return {"msg": "Access denied"}, 403

    data = request.get_json(silent=True)
    if not data:
        return {"msg": "JSON body required"}, 400
    new_status = data.get("status")

    if not new_status:
        return {"msg": "status is required"}, 400

    complaint = db.session.get(Complaint, complaint_id)
    if not complaint:
        abort(404)

    if not is_valid_transition(complaint.status, new_status):
        return {"msg": "Invalid status transition"}, 400

    complaint.status = new_status
    db.session.commit()

    return {
        "msg": "Status updated",
        "complaint_id": complaint.id,
        "status": complaint.status
    }
