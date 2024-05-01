import datetime as dt
import uuid
from typing import Annotated

from fastapi import APIRouter, Form
from sqlmodel import SQLModel

from lifehub.api.lib.user import (
    authenticate_user,
    create_user,
    get_access_token,
)
from lifehub.api.routers.dependencies import SessionDep, UserDep
from lifehub.models.user import User

router = APIRouter()


class UserLogin(SQLModel):
    user_id: uuid.UUID
    name: str
    access_token: str
    expires_at: dt.datetime


@router.post("/login", response_model=UserLogin)
async def user_login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    user = authenticate_user(username, password)
    token = get_access_token(user)
    login = UserLogin(
        user_id=user.id,
        name=user.name,
        access_token=token.access_token,
        expires_at=token.expires_at,
    )
    return login


@router.post("/signup", response_model=UserLogin)
async def user_signup(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    name: Annotated[str, Form()],
):
    new_user: User = create_user(username, password, name)
    token = get_access_token(new_user)
    login = UserLogin(
        user_id=new_user.id,
        name=new_user.name,
        access_token=token.access_token,
        expires_at=token.expires_at,
    )
    return login


@router.delete("/me")
async def delete_user(user: UserDep, session: SessionDep):
    user = session.merge(user)
    session.delete(user)
    session.commit()
