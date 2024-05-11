import datetime as dt
from os import getenv

import argon2
from jose import jwt


def hash_password(password: str) -> str:
    return argon2.PasswordHasher().hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return argon2.PasswordHasher().verify(hashed_password, password)
    except argon2.exceptions.VerifyMismatchError:
        return False


def create_jwt_token(username: str, expires_at: dt.datetime) -> str:
    secret_key: str | None = getenv("AUTH_SECRET_KEY")
    algorithm: str | None = getenv("AUTH_ALGORITHM")

    if secret_key is None or algorithm is None:
        # TODO: Service exception (#27)
        raise Exception("JWT secret key or algorithm not set")

    return jwt.encode(
        {"sub": username, "exp": expires_at}, secret_key, algorithm=algorithm
    )


def decode_jwt_token(token: str) -> dict:
    secret_key: str | None = getenv("AUTH_SECRET_KEY")
    algorithm: str | None = getenv("AUTH_ALGORITHM")

    if secret_key is None or algorithm is None:
        # TODO: Service exception (#27)
        raise Exception("JWT secret key or algorithm not set")

    return jwt.decode(token, secret_key, algorithms=[algorithm])
