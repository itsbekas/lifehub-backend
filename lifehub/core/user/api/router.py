from typing import Annotated

from fastapi import APIRouter, Form

from lifehub.core.user.api.dependencies import UserDep, UserServiceDep
from lifehub.core.user.models import UserTokenResponse
from lifehub.core.user.service.user import UserService

router = APIRouter()


@router.post("/login", response_model=UserTokenResponse)
async def user_login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    user_service: UserServiceDep,
):
    try:
        user = user_service.login_user(username, password)
        user_token = user_service.create_access_token(user)
    except Exception as e:
        # TODO: API Exception (#28)
        raise e
    return user_token


@router.post("/signup", response_model=UserTokenResponse)
async def user_signup(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    name: Annotated[str, Form()],
    user_service: UserServiceDep,
):
    user_service = UserService()
    try:
        user = user_service.create_user(username, password, name)
        user_token = user_service.create_access_token(user)
    except Exception as e:
        # TODO: API Exception (#28)
        raise e
    return user_token


@router.delete("/me")
async def delete_user(user: UserDep, user_service: UserServiceDep):
    user_service.delete_user(user)