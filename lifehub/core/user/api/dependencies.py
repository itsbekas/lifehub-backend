from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from lifehub.core.user.schema import User
from lifehub.core.user.service.user import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

UserServiceDep = Annotated[UserService, Depends(UserService)]


def get_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: UserServiceDep,
) -> User:
    try:
        user = user_service.authenticate_user(token)
    except Exception:
        raise HTTPException(401, "Invalid token")

    return user


UserDep = Annotated[User, Depends(get_user)]
