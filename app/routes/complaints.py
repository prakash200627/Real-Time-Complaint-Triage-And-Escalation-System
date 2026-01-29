from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Complaint
from app.services.ai_service import analyze_complaint
from app.services.escalation_service import escalate_complaint


complaints_bp = Blueprint(
    "complaints",
    __name__,
    url_prefix="/complaints"
)


@complaints_bp.route("", methods=["POST"])
@jwt_required()
def create_complaint():
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True)

    if not data:
        return {"msg": "JSON body required"}, 400

    title = data.get("title")
    description = data.get("description")

    if not title or not description:
        return {"msg": "title and description required"}, 400

    analysis = analyze_complaint(f"{title} {description}")

    complaint = Complaint(
        user_id=user_id,
        title=title,
        description=description,
        category=analysis["category"],
        priority=analysis["priority"],
        confidence=analysis.get("confidence", 0.0),
        status="open"
    )


    db.session.add(complaint)
    
    db.session.flush()

    if analysis["priority"] == "high" and analysis.get("confidence", 0) >= 0.6:
        escalate_complaint(
            complaint,
            reason="High confidence AI escalation"
        )


    db.session.commit()


    return jsonify({
        "message": "Complaint created successfully",
        "complaint_id": complaint.id,
        "category": analysis["category"],
        "priority": analysis["priority"]
    }), 201


@complaints_bp.route("/my", methods=["GET"])
@jwt_required()
def get_my_complaints():
    user_id = int(get_jwt_identity())

    complaints = Complaint.query.filter_by(user_id=user_id).all()

    return jsonify([
        {
            "id": c.id,
            "title": c.title,
            "category": c.category,
            "priority": c.priority,
            "status": c.status,
            "created_at": c.created_at.isoformat()
        } for c in complaints
    ])
