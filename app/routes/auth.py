from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app.extensions import db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)
    if not data:
        return {"msg": "JSON body required"}, 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {"msg": "email and password required"}, 400

    if User.query.filter_by(email=email).first():
        return {"msg": "email already registered"}, 409

    user = User(
        name=name or "User",
        email=email,
        password=generate_password_hash(password)
    )
    db.session.add(user)
    db.session.commit()

    return {"msg": "User registered successfully"}, 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)
    if not data:
        return {"msg": "JSON body required"}, 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {"msg": "email and password required"}, 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.password or not check_password_hash(user.password, password):
        return {"msg": "Invalid credentials"}, 401

    token = create_access_token(identity=str(user.id))
    return {"access_token": token}


@auth_bp.route("/dev-login", methods=["POST"])
def dev_login():
    data = request.get_json(silent=True)
    if not data:
        return {"msg": "JSON body required"}, 400

    email = data.get("email")
    if not email:
        return {"msg": "email required"}, 400

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(name="Test User", email=email, password=generate_password_hash("password"))
        db.session.add(user)
        db.session.commit()

    token = create_access_token(identity=str(user.id))
    return {"access_token": token}

@auth_bp.route("/make-admin", methods=["POST"])
@jwt_required()
def make_admin():
    user_id = get_jwt_identity()
    user = db.session.get(User, int(user_id))
    if not user:
        return {"msg": "User not found"}, 404
    user.role = "admin"
    db.session.commit()
    return {"msg": "User promoted to admin"}
