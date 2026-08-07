#!/usr/bin/env python3
"""Create database tables for PlanVenture API.

Run from the `planventure-api` directory:

    python3 scripts/create_db.py

"""
from __future__ import annotations

from app import app, db

# Import the models package so all modules (User, Trip, etc.) are registered
import models  # noqa: F401


def main() -> None:
    with app.app_context():
        db.create_all()
        print("Database tables created (if not existing).")


if __name__ == "__main__":
    main()
