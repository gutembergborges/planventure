import re

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from app import db
from models import User

bp = Blueprint("auth", __name__, url_prefix="/auth")


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"msg": "Email and password are required"}), 400

    if not EMAIL_RE.match(email):
        return jsonify({"msg": "Invalid email address"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already registered"}), 409

    user = User(email=email)
    user.password = password
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=user.id)

    return jsonify({"access_token": token, "user": user.to_dict()}), 201
