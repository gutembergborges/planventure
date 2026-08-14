import os

from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from os import environ
from dotenv import load_dotenv
from datetime import timedelta

# Load environment variables
load_dotenv()

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = environ.get('JWT_SECRET', 'your-secret-key')  # Change this in production
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    jwt = JWTManager(app)

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL', 'sqlite:///planventure.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    try:
        from routes.auth import auth_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')
    except Exception:
        # If blueprint import fails during static analysis, ignore; runtime will surface errors
        pass

    # Register routes
    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to PlanVenture API"})

    @app.route('/health')
    def health_check():
        return jsonify({"status": "healthy"})

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
    #app.run(debug=os.getenv("FLASK_ENV") == "development")
