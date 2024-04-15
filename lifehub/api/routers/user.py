from typing import Annotated

from fastapi import APIRouter, Form

from lifehub.api.lib.user import (
    authenticate_user,
    create_user,
    get_access_token,
)
from lifehub.models.user import UserToken

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post("/login", response_model=UserToken)
async def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    user = authenticate_user(username, password)
    token = get_access_token(user)
    return token


@router.post("/signup", response_model=UserToken)
async def signup(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    name: Annotated[str, Form()],
):
    new_user = create_user(username, password, name)
    token = get_access_token(new_user)
    return token
