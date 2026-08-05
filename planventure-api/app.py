import os

from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from os import environ
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
# app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///planventure.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Import models so they are registered with SQLAlchemy before create_all()
try:
    from models import User  # noqa: F401
except Exception:
    # Import errors may occur during static analysis or early import; ignore at runtime
    pass

@app.route("/")
def home():
    return jsonify({"message": "Welcome to PlanVenture API"})

@app.route("/health")
def health_check():
    return jsonify({"status": "healthy"})

# @app.route("/db-health")
# def db_health():
#     try:
#         db.session.execute(db.text("SELECT 1"))
#         return jsonify({"status": "healthy", "database": "connected"})
#     except Exception as exc:
#         return jsonify({"status": "error", "database": "disconnected", "error": str(exc)}), 500

if __name__ == "__main__":
    with app.app_context():
        # Create all database tables if they don't exist
        db.create_all()
    app.run(debug=True)
    #app.run(debug=os.getenv("FLASK_ENV") == "development")

# class HealthCheck(db.Model):
#     __tablename__ = "health_checks"

#     id = db.Column(db.Integer, primary_key=True)
#     status = db.Column(db.String(50), nullable=False, default="healthy")
