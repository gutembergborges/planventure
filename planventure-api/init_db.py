
from app import create_app, db
import models  # ensure all models are imported and registered


def init_db():
    # Initialize the database and create tables.
    app = create_app()
    with app.app_context():
        # Create all database tables if they don't exist
        db.create_all()
        print("Database initialized and tables created.")

if __name__ == "__main__":
    init_db()
