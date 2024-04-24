from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, status

from lifehub.api.lib.user import (
    authenticate_user,
    create_user,
    get_access_token,
)
from lifehub.api.routers.dependencies import SessionDep, UserDep
from lifehub.clients.db.util import ModuleDBClient
from lifehub.models.user import User, UserToken
from lifehub.models.util import Module

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


class ModuleDoesNotExistException(HTTPException):
    def __init__(self, module: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Module {module} does not exist",
        )


class UserDoesNotHaveProvidersException(HTTPException):
    def __init__(self, providers: list[str]):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User does not have providers: {', '.join(providers)}",
        )


def verify_module(module_name: str) -> Module:
    db_client = ModuleDBClient()
    m = db_client.get_by_name(module_name)
    if not m:
        raise ModuleDoesNotExistException(module_name)
    return m


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
    new_user: User = create_user(username, password, name)
    token = get_access_token(new_user)
    return token


@router.post("/module")
async def add_module(
    user: UserDep,
    session: SessionDep,
    module: Annotated[Module, Depends(verify_module)],
):
    user = session.merge(user)
    module = session.merge(module)

    missed_providers = []

    for provider in module.providers:
        if provider not in user.providers:
            missed_providers.append(provider.name)

    if missed_providers:
        raise UserDoesNotHaveProvidersException(missed_providers)

    user.modules.append(module)
    session.add(user)
    session.commit()
