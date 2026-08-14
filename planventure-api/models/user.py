from datetime import datetime, timezone

from app import db
from utils.auth import hash_password, verify_password


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Add relationship
    trips = db.relationship('Trip', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password: str) -> None:
        """Hash and set the user's password."""
        # store the bcrypt hash as a UTF-8 string
        self.password_hash = hash_password(password)

    def check_password(self, password: str) -> bool:
        """Return True if the provided password matches the stored hash."""
        if not self.password_hash:
            return False
        return verify_password(password, self.password_hash)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
