import datetime as dt
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy import exc as sa_exc
from sqlmodel import SQLModel

from lifehub.api.lib.user import (
    authenticate_user,
    create_user,
    get_access_token,
)
from lifehub.api.routers.dependencies import ProviderDep, SessionDep, UserDep
from lifehub.clients.db.provider.api_token import APITokenDBClient
from lifehub.clients.db.util import ModuleDBClient
from lifehub.models.provider.provider import Provider, ProviderType
from lifehub.models.user import User, UserToken
from lifehub.models.util import Module

router = APIRouter()


class UserLogin(SQLModel):
    user_id: uuid.UUID
    name: str
    access_token: str
    expires_at: dt.datetime


def verify_module(module_name: str, session: SessionDep) -> Module:
    module = ModuleDBClient(session).get_by_name(module_name)
    if not module:
        raise HTTPException(404, f"Module {module_name} does not exist")
    return module


@router.post("/login", response_model=UserLogin)
async def login(
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


@router.post("/signup", response_model=UserToken)
async def signup(
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
        raise HTTPException(
            403, f"User is missing providers: {', '.join(missed_providers)}"
        )

    user.modules.append(module)
    session.add(user)

    try:
        session.commit()
    except sa_exc.IntegrityError as e:
        session.rollback()
        match e.orig.errno:
            case 1062:
                raise HTTPException(409, f"User already has module {module.name}")
            case _:
                raise e


class ProviderWithModules(SQLModel):
    id: int
    name: str
    type: ProviderType
    modules: list[Module]


@router.get("/providers", response_model=list[ProviderWithModules])
async def get_user_providers(user: UserDep):
    return user.providers


@router.delete("/providers/{provider_id}")
async def remove_user_provider(
    user: UserDep,
    session: SessionDep,
    provider: ProviderDep,
):
    user = session.merge(user)
    provider = session.merge(provider)

    if provider not in user.providers:
        raise HTTPException(404, f"User does not have provider {provider.name}")

    # Remove Provider from User
    user.providers.remove(provider)
    # Remove Modules that require Provider from User
    user.modules = [module for module in user.modules if module not in provider.modules]
    # Remove APITokens for Provider from User
    token = APITokenDBClient(session).get(user, provider)
    session.delete(token)

    session.add(user)
    session.commit()


class ModuleWithProviders(SQLModel):
    id: int
    name: str
    providers: list[Provider]


@router.get("/modules", response_model=list[ModuleWithProviders])
async def get_user_modules(user: UserDep):
    return user.modules
