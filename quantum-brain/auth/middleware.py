"""
ThaleOS Auth Middleware
FastAPI Depends functions for JWT validation and RBAC.
"""

import logging
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import db
from .service import decode_access_token

logger = logging.getLogger("ThaleOS.Auth")

_bearer = HTTPBearer(auto_error=False)

ROLE_RANK = {"readonly": 0, "user": 1, "admin": 2}


def _load_user(user_id: str) -> dict:
    user = db.fetchone("SELECT * FROM users WHERE id = ?", (user_id,))
    if not user or user["disabled"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or disabled",
        )
    return user


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_bearer),
) -> dict:
    """
    Require a valid JWT access token. Returns the user dict from DB.
    Raises 401 if missing or invalid.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid or expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return _load_user(payload["sub"])


async def optional_auth(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_bearer),
) -> Optional[dict]:
    """
    Like get_current_user but returns None instead of raising if no token.
    Use on endpoints that work both authenticated and anonymous.
    """
    if credentials is None:
        return None
    payload = decode_access_token(credentials.credentials)
    if payload is None:
        return None
    try:
        return _load_user(payload["sub"])
    except HTTPException:
        return None


def require_role(minimum_role: str):
    """
    Dependency factory — ensures the caller has at least `minimum_role`.
    Usage:
        @app.post("/admin-only")
        async def endpoint(user = Depends(require_role("admin"))): ...
    """
    async def _check(user: dict = Depends(get_current_user)) -> dict:
        user_rank = ROLE_RANK.get(user["role"], 0)
        required_rank = ROLE_RANK.get(minimum_role, 99)
        if user_rank < required_rank:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires {minimum_role} role (you have {user['role']})",
            )
        return user
    return _check
