import datetime as dt
import uuid
from typing import Annotated

from fastapi import APIRouter, Form
from sqlmodel import SQLModel

from lifehub.core.api_dependencies import SessionDep, UserDep
from lifehub.core.user.service import (
    authenticate_user,
    create_access_token,
    create_user,
)
from lifehub.models.user_old import User, UserTokenResponse

router = APIRouter()


class UserLogin(SQLModel):
    user_id: uuid.UUID
    name: str
    access_token: str
    expires_at: dt.datetime


@router.post("/login", response_model=UserTokenResponse)
async def user_login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    user = authenticate_user(username, password)
    return create_access_token(user)


@router.post("/signup", response_model=UserTokenResponse)
async def user_signup(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    name: Annotated[str, Form()],
):
    user: User = create_user(username, password, name)
    return create_access_token(user)


@router.delete("/me")
async def delete_user(user: UserDep, session: SessionDep):
    user = session.merge(user)
    session.delete(user)
    session.commit()
