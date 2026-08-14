"""Password hashing utilities for PlanVenture.

Provides small helpers around bcrypt to produce and verify password hashes
and to generate salts. Hashes are returned as UTF-8 strings so they can be
stored in text columns.
"""
from __future__ import annotations

import os
from typing import Optional

import bcrypt


def _get_rounds() -> int:
    try:
        return int(os.getenv("BCRYPT_ROUNDS", "12"))
    except Exception:
        return 12


def generate_salt(rounds: Optional[int] = None) -> bytes:
    """Return a bcrypt salt (bytes)."""
    if rounds is None:
        rounds = _get_rounds()
    return bcrypt.gensalt(rounds)


def hash_password(password: str, salt: Optional[bytes] = None, rounds: Optional[int] = None) -> str:
    """Hash `password` and return the hash as a UTF-8 string.

    If `salt` is not provided, one will be generated using `rounds` or the
    `BCRYPT_ROUNDS` environment variable.
    """
    if salt is None:
        if rounds is None:
            rounds = _get_rounds()
        salt = bcrypt.gensalt(rounds)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(password: str, stored_hash: str) -> bool:
    """Return True when `password` matches `stored_hash`.

    `stored_hash` should be the UTF-8 string as returned by `hash_password`.
    """
    if isinstance(stored_hash, str):
        stored = stored_hash.encode("utf-8")
    else:
        stored = stored_hash
    try:
        return bcrypt.checkpw(password.encode("utf-8"), stored)
    except ValueError:
        return False
