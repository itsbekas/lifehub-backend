import datetime as dt
import os

import argon2
from argon2 import PasswordHasher
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from lifehub.clients.db.service import get_session
from lifehub.clients.db.user import UserDBClient, UserTokenDBClient
from lifehub.models.user import User, UserToken

from ..exceptions.user import CredentialsException, UserExistsException

AUTH_SECRET_KEY = os.environ["AUTH_SECRET_KEY"]
AUTH_ALGORITHM = os.environ["AUTH_ALGORITHM"]

ph = PasswordHasher()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")


def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, password)
    except argon2.exceptions.VerifyMismatchError:
        return False


def get_user(username: str) -> User | None:
    with get_session() as session:
        db_client = UserDBClient(session)
        return db_client.get_by_username(username)


def add_user(user: User) -> User:
    with get_session() as session:
        db_client = UserDBClient(session)
        db_client.add(user)
        db_client.commit()
        db_client.refresh(user)
        return user


def authenticate_user(username: str, password: str) -> User | None:
    user = get_user(username)
    if not user or not verify_password(password, user.password):
        raise CredentialsException()
    return user


def create_user(username: str, password: str, name: str) -> User:
    hashed_password = hash_password(password)
    user = get_user(username)
    if user:
        raise UserExistsException()
    new_user = User(username=username, password=hashed_password, name=name)
    return add_user(new_user)


def create_access_token(user: User) -> UserToken:
    created_at = dt.datetime.now()
    expires_at = created_at + dt.timedelta(days=30)
    jwtoken = jwt.encode(
        {"sub": user.username, "exp": expires_at},
        AUTH_SECRET_KEY,
        algorithm=AUTH_ALGORITHM,
    )
    token = UserToken(
        user_id=user.id,
        access_token=jwtoken,
        token_type="bearer",
        created_at=created_at,
        expires_at=expires_at,
    )
    with get_session() as session:
        db_client = UserTokenDBClient(user, session)
        db_client.add(token)
        db_client.commit()
        db_client.refresh(token)
    return token


def get_access_token(user: User) -> UserToken:
    with get_session() as session:
        db_client = UserTokenDBClient(user, session)
        token = db_client.get_one_or_none()
    if token and token.expires_at > dt.datetime.now():
        return token
    return create_access_token(user)
