from typing import Annotated

from fastapi import APIRouter, Depends, Form
from sqlmodel import Session

from lifehub.api.lib.user import (
    authenticate_user,
    create_access_token,
    create_user,
)
from lifehub.lib.db import get_session
from lifehub.lib.models.user import UserToken

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post("/login", response_model=UserToken)
async def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    session: Session = Depends(get_session),
):
    user = authenticate_user(session, username, password)
    token = create_access_token(user)
    return token


@router.post("/signup", response_model=UserToken)
async def signup(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    name: Annotated[str, Form()],
    session: Session = Depends(get_session),
):
    new_user = create_user(session, username, password, name)
    token = create_access_token(new_user)
    print(token)
    return token
