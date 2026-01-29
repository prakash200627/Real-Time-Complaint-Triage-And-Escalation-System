from flask import Flask, jsonify
from .extensions import db, jwt
from flask_migrate import Migrate
from dotenv import load_dotenv


load_dotenv()

def create_app(config_object: str = "config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    jwt.init_app(app)
    Migrate(app, db)

    from . import models   

    from .routes.auth import auth_bp
    from .routes.complaints import complaints_bp
    from .routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(complaints_bp)
    app.register_blueprint(admin_bp)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @jwt.unauthorized_loader
    def _unauthorized(reason):
        return jsonify({"msg": "Missing or invalid Authorization header", "detail": reason}), 401

    @jwt.invalid_token_loader
    def _invalid_token(reason):
        return jsonify({"msg": "Invalid token", "detail": reason}), 422

    @jwt.expired_token_loader
    def _expired_token(jwt_header, jwt_payload):
        return jsonify({"msg": "Token has expired"}), 401

    @jwt.revoked_token_loader
    def _revoked_token(jwt_header, jwt_payload):
        return jsonify({"msg": "Token has been revoked"}), 401

    return app
