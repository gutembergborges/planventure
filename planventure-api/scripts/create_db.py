#!/usr/bin/env python3
"""Create database tables for PlanVenture API.

Run from the `planventure-api` directory:

    python3 scripts/create_db.py

"""
from __future__ import annotations

from app import app, db

# Import models so SQLAlchemy registers them before create_all()
try:
    # models package exposes User via models/__init__.py
    from models import User  # noqa: F401
except Exception:
    # fallback: import the user module directly
    import models.user  # noqa: F401


def main() -> None:
    with app.app_context():
        db.create_all()
        print("Database tables created (if not existing).")


if __name__ == "__main__":
    main()
