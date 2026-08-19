from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'msg': 'Invalid token'}), 401
    return decorated

def get_current_user_id():
    return get_jwt_identity()


def protect_blueprint(bp):
    """Register a `before_request` handler on a Blueprint to require JWT for all its routes.

    Usage:
        from utils.auth import protect_blueprint
        protect_blueprint(my_blueprint)
    """
    @bp.before_request
    def _require_jwt():
        try:
            verify_jwt_in_request()
        except Exception:
            return jsonify({'msg': 'Invalid or missing token'}), 401