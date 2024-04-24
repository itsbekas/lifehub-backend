from typing import Annotated

from fastapi import Depends
from jose import JWTError, jwt
from sqlmodel import Session

from lifehub.api.lib.user import (
    AUTH_ALGORITHM,
    AUTH_SECRET_KEY,
    CredentialsException,
    oauth2_scheme,
)
from lifehub.clients.db.service import get_session
from lifehub.clients.db.user import UserDBClient
from lifehub.models.user import User


def yield_session():
    with get_session() as session:
        yield session


SessionDep = Annotated[Session, Depends(yield_session)]


def get_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep,
) -> User:
    try:
        payload = jwt.decode(token, AUTH_SECRET_KEY, algorithms=[AUTH_ALGORITHM])
    except JWTError:
        raise CredentialsException()

    db_client = UserDBClient(session)
    user = db_client.get_by_username(payload.get("sub"))
    if user is None:
        raise CredentialsException()
    return user


UserDep = Annotated[User, Depends(get_user)]
