import datetime as dt
import os

import argon2
from argon2 import PasswordHasher
from fastapi import HTTPException, status
from jose import jwt
from sqlmodel import Session, select

from lifehub.lib.models.user import User, UserToken

AUTH_SECRET_KEY = os.environ["AUTH_SECRET_KEY"]
AUTH_ALGORITHM = os.environ["AUTH_ALGORITHM"]

ph = PasswordHasher()


class CredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, password)
    except argon2.exceptions.VerifyMismatchError:
        return False


def authenticate_user(session: Session, username: str, password: str) -> User | None:
    query = select(User).where(User.username == username)
    user = session.exec(query).first()
    if not user or not verify_password(password, user.password):
        raise CredentialsException()
    return user


def create_user(session: Session, username: str, password: str, name: str) -> User:
    hashed_password = hash_password(password)
    new_user = User(username=username, password=hashed_password, name=name)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


def create_access_token(user: User) -> UserToken:
    token = jwt.encode(
        {"sub": user.username, "exp": dt.datetime.now() + dt.timedelta(days=30)},
        AUTH_SECRET_KEY,
        algorithm=AUTH_ALGORITHM,
    )
    return UserToken(user_id=user.id, token=token)
