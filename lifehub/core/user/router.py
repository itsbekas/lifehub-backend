from typing import Annotated

from fastapi import APIRouter, Form

from lifehub.core.common.api.dependencies import SessionDep, UserDep
from lifehub.core.user.models import UserTokenResponse
from lifehub.core.user.schema import User
from lifehub.core.user.service import (
    authenticate_user,
    create_access_token,
    create_user,
)

router = APIRouter()


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
