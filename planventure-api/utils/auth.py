from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models import User

def auth_middleware(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            # This will raise a JWT-specific error that the JWTManager handlers convert to JSON
            verify_jwt_in_request()

            # get_jwt_identity() returns whatever was stored as identity (we expect user id)
            identity = get_jwt_identity()
            if identity is None:
                return jsonify({'error': 'Invalid token identity'}), 401

            # Safely coerce to int if possible
            try:
                user_id = int(identity)
            except Exception:
                return jsonify({'error': 'Invalid token identity type'}), 401

            # Check if user still exists in the database
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 401

            # Attach current user for route convenience
            g.current_user = user

            return f(*args, **kwargs)
        except Exception:
            # Let JWTManager handlers provide more specific messages where possible.
            return jsonify({'error': 'Invalid or missing token'}), 401
    return decorated

def get_current_user_id():
    return get_jwt_identity()
