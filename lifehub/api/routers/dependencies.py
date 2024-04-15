from typing import Annotated

from fastapi import Depends
from lifehub.clients.db.db_service import DatabaseService
from lifehub.api.lib.user import CredentialsException, oauth2_scheme, AUTH_ALGORITHM, AUTH_SECRET_KEY
from jose import JWTError, jwt
import uuid


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
    user = db_service.get_user_by_username(username)
    if user is None:
        raise CredentialsException()
    return user.id
