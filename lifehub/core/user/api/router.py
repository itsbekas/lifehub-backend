from typing import Annotated

from fastapi import APIRouter, Form, HTTPException

from lifehub.core.common.api.dependencies import SessionDep
from lifehub.core.user.api.dependencies import UserDep, UserServiceDep
from lifehub.core.user.models import UserTokenResponse
from lifehub.core.user.service.user import UserService, UserServiceException

router = APIRouter()


@router.post("/login")
async def user_login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    user_service: UserServiceDep,
) -> UserTokenResponse:
    try:
        user = user_service.login_user(username, password)
    except UserServiceException as e:
        raise HTTPException(status_code=401, detail=str(e))
    user_token = user_service.create_access_token(user)
    return user_token


@router.post("/signup")
async def user_signup(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    name: Annotated[str, Form()],
    user_service: UserServiceDep,
    session: SessionDep,
) -> UserTokenResponse:
    user_service = UserService(session)
    try:
        user = user_service.create_user(username, password, name)
    except UserServiceException as e:
        raise HTTPException(status_code=403, detail=str(e))
    user_token = user_service.create_access_token(user)
    return user_token


@router.delete("/me")
async def delete_user(user: UserDep, user_service: UserServiceDep) -> None:
    user_service.delete_user(user)
