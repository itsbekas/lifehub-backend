import uuid
from typing import Annotated

from fastapi import Depends
from jose import JWTError, jwt

from lifehub.api.lib.user import (
    AUTH_ALGORITHM,
    AUTH_SECRET_KEY,
    CredentialsException,
    oauth2_scheme,
)
from lifehub.clients.db.db_service import DatabaseService
from lifehub.clients.db.user import UserDBClient

db_service = DatabaseService()


def get_session():
    session = db_service.get_session()
    try:
        yield session
    finally:
        session.close()


def get_user_id(token: Annotated[str, Depends(oauth2_scheme)]) -> uuid.UUID:
    try:
        payload = jwt.decode(token, AUTH_SECRET_KEY, algorithms=[AUTH_ALGORITHM])
    except JWTError:
        raise CredentialsException()
    username = payload.get("sub")
    db_client = UserDBClient()
    user = db_client.get_by_username(username)
    if user is None:
        raise CredentialsException()
    return user.id
