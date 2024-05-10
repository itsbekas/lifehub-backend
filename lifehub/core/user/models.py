import datetime as dt

from pydantic.dataclasses import dataclass


@dataclass
class UserLoginRequest:
    username: str
    password: str


@dataclass
class UserCreateRequest:
    username: str
    password: str
    name: str


@dataclass
class UserTokenResponse:
    name: str
    access_token: str
    expires_at: dt.datetime
