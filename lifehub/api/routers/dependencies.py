from typing import Annotated

from fastapi import Depends
from lifehub.clients.db.db_service import DatabaseService
from lifehub.api.lib.user import CredentialsException, oauth2_scheme, AUTH_ALGORITHM, AUTH_SECRET_KEY
from jose import JWTError, jwt
import uuid

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
    except JWTError as e:
        raise CredentialsException()
    username = payload.get("sub")
    db_client = UserDBClient()
    user = db_client.get_by_username(username)
    if user is None:
        raise CredentialsException()
    return user.id
