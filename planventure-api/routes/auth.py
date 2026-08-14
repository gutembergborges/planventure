from flask import Blueprint, request, jsonify
from app import db
from models import User
from utils.validators import validate_email

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}

    # Validate required fields
    if not all(k in data for k in ('email', 'password')):
        return jsonify({'error': 'Missing required fields'}), 400

    # Validate email format
    if not validate_email(data['email']):
        return jsonify({'error': 'Invalid email address format'}), 400

    # Check if the email and user are already exist
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409

    # Create a new user
    try:
        user = User(email=data['email'])
        user.password = data['password']    # This will hash the password
        db.session.add(user)
        db.session.commit()

        # Generate auth JWT token
        token = user.generate_auth_token()
        return jsonify({
            'msg': 'User registered successfully', 
            'token': token
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed: Error creating user'}), 500
