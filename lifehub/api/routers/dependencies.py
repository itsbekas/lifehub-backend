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
from lifehub.clients.db.service import DatabaseService
from lifehub.clients.db.user import UserDBClient
from lifehub.models.user import User


def get_session():
    db_service = DatabaseService()
    with db_service.get_session() as session:
        yield session


def user_is_authenticated(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    try:
        payload = jwt.decode(token, AUTH_SECRET_KEY, algorithms=[AUTH_ALGORITHM])
    except JWTError:
        raise CredentialsException()
    return payload.get("sub")


def get_user(username: Annotated[str, user_is_authenticated]) -> User:
    db_client = UserDBClient()
    user = db_client.get_by_username(username)
    if user is None:
        raise CredentialsException()
    return user


UserDep = Annotated[uuid.UUID, Depends(get_user)]
