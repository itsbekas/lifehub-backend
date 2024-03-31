from typing import Annotated
from os import getenv
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from argon2 import PasswordHasher
from pydantic import BaseModel

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

users_db = {
    "bekas": {
        "username": "bekas",
        "name": "Bernardo",
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$FxzS+hhC02MMTCjYWtrnuQ$gDoGJxJKWvE7bV6Loi43/42sQ49CGT1CgWqIrSw5bk8",
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str


class UserInDB(User):
    hashed_password: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
pw_hasher = PasswordHasher()


class CredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


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


@router.get("/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.post("/token", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        raise CredentialsException()
    expires_delta = timedelta(days=30)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=expires_delta
    )
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=expires_delta.total_seconds()
    )
