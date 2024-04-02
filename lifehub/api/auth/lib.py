from datetime import datetime, timedelta, timezone
from os import getenv
from typing import Annotated

from argon2 import PasswordHasher
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from .models import TokenData, User, UserInDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
pw_hasher = PasswordHasher()

users_db = {
    "bekas": {
        "username": "bekas",
        "name": "Bernardo",
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$FxzS+hhC02MMTCjYWtrnuQ$gDoGJxJKWvE7bV6Loi43/42sQ49CGT1CgWqIrSw5bk8",
    }
}


class CredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    try:
        payload = jwt.decode(
            token, getenv("AUTH_SECRET_KEY"), algorithms=[getenv("AUTH_ALGORITHM")]
        )
        username: str = payload.get("sub")
        if username is None:
            raise CredentialsException()
        token_data = TokenData(username=username)
    except JWTError:
        raise CredentialsException()
    user = get_user(users_db, username=token_data.username)
    if user is None:
        raise CredentialsException("User not found")
    return user


def verify_password(plain_password, hashed_password):
    return pw_hasher.verify(hashed_password, plain_password)


def get_password_hash(password):
    return pw_hasher.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(users_db, username: str, password: str):
    user = get_user(users_db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, getenv("AUTH_SECRET_KEY"), algorithm=getenv("AUTH_ALGORITHM")
    )
