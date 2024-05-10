import datetime as dt
from os import getenv

import argon2
from jose import JWTError, jwt

from lifehub.core.common.base_service import BaseService
from lifehub.core.user.models import UserTokenResponse
from lifehub.core.user.repository.user import UserRepository
from lifehub.core.user.schema import User


class UserService(BaseService):
    def __init__(self):
        super().__init__()
        self.user_repository = UserRepository(self.session)
        self.password_hasher = argon2.PasswordHasher()

    def create_user(self, username: str, password: str, name: str) -> User:
        user = self.user_repository.get_by_username(username)

        if user is not None:
            # TODO: Service exception (#27)
            raise Exception("User already exists")

        hashed_password = self.hash_password(password)

        new_user = User(username=username, password=hashed_password, name=name)
        self.user_repository.add(new_user)
        self.user_repository.commit()
        self.user_repository.refresh(new_user)

        return new_user

    def create_access_token(self, user: User) -> UserTokenResponse:
        expires_at = dt.datetime.now() + dt.timedelta(days=30)

        return UserTokenResponse(
            name=user.name,
            access_token=self.create_jwt_token(user.username, expires_at),
            expires_at=expires_at,
        )

    def login_user(self, username: str, password: str) -> User:
        user: User | None = self.user_repository.get_by_username(username)

        if user is None or not self.verify_password(password, user.password):
            # TODO: Service exception (#27)
            raise Exception("Invalid credentials")

        return user

    def authenticate_user(self, token: str) -> User:
        try:
            payload = self.decode_jwt_token(token)
        except JWTError:
            # TODO: Service exception (#27)
            raise Exception("Invalid token")

        username: str = payload.get("sub")  # type: ignore

        user: User | None = self.user_repository.get_by_username(username)

        if user is None:
            # TODO: Service exception (#27)
            raise Exception("User not found")

        return user

    def delete_user(self, user: User) -> None:
        self.user_repository.delete(user)
        self.user_repository.commit()

    def hash_password(self, password: str) -> str:
        return self.password_hasher.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        try:
            return self.password_hasher.verify(hashed_password, password)
        except argon2.exceptions.VerifyMismatchError:
            return False

    def create_jwt_token(self, username: str, expires_at: dt.datetime) -> str:
        secret_key: str | None = getenv("AUTH_SECRET_KEY")
        algorithm: str | None = getenv("AUTH_ALGORITHM")

        if secret_key is None or algorithm is None:
            # TODO: Service exception (#27)
            raise Exception("JWT secret key or algorithm not set")

        return jwt.encode(
            {"sub": username, "exp": expires_at}, secret_key, algorithm=algorithm
        )

    def decode_jwt_token(self, token: str) -> dict:
        secret_key: str | None = getenv("AUTH_SECRET_KEY")
        algorithm: str | None = getenv("AUTH_ALGORITHM")

        if secret_key is None or algorithm is None:
            # TODO: Service exception (#27)
            raise Exception("JWT secret key or algorithm not set")

        return jwt.decode(token, secret_key, algorithms=[algorithm])

    def __del__(self):
        self.user_repository.close()
