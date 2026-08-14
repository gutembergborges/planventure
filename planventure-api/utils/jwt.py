"""JWT helpers for PlanVenture API.

Provides `create_access_token` and `verify_access_token` helpers using
`pyjwt` (the `jwt` package). Tokens are signed with a secret from
`JWT_SECRET` environment variable and use HS256.
"""
from __future__ import annotations

import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

import jwt


JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXP_MINUTES = int(os.getenv("JWT_EXP_MINUTES", "60"))


def create_access_token(sub: str, extra_claims: Optional[Dict[str, Any]] = None, expires_delta: Optional[timedelta] = None) -> str:
    now = datetime.utcnow()
    if expires_delta is None:
        expires_delta = timedelta(minutes=JWT_EXP_MINUTES)
    payload = {
        "sub": str(sub),
        "iat": now,
        "exp": now + expires_delta,
    }
    if extra_claims:
        payload.update(extra_claims)
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    # jwt.encode may return bytes or str depending on the library version
    if isinstance(token, bytes):
        return token.decode("utf-8")
    return token


def verify_access_token(token: str) -> Dict[str, Any]:
    """Verify the token and return the decoded payload. Raises jwt exceptions on failure."""
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
