from flask_jwt_extended import get_jwt_identity
from app.extensions import db
from app.models import User

def get_current_user():
    user_id = get_jwt_identity()
    if user_id is None:
        return None
    return db.session.get(User, int(user_id))

def require_roles(*roles):
    def wrapper(user):
        return user and user.role in roles
    return wrapper

def user_has_role(user, *roles):
    return user and user.role in roles
