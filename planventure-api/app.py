import os

from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from os import environ
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Database configuration
    # # app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///planventure.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)

    # Register routes
    @app.route("/")
    def home():
        return jsonify({"message": "Welcome to PlanVenture API"})

    #@app.route("/health")
    #def health_check():
    #    return jsonify({"status": "healthy"})

    return app

# @app.route("/db-health")
# def db_health():
#     try:
#         db.session.execute(db.text("SELECT 1"))
#         return jsonify({"status": "healthy", "database": "connected"})
#     except Exception as exc:
#         return jsonify({"status": "error", "database": "disconnected", "error": str(exc)}), 500

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
    #app.run(debug=os.getenv("FLASK_ENV") == "development")
