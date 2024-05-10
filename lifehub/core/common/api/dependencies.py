from typing import Annotated

from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from sqlalchemy import Session

from lifehub.clients.db.repository.provider import ProviderDBClient
from lifehub.clients.db.user import UserDBClient
from lifehub.core.common.api.exceptions import (
    ProviderDoesNotExistException,
    ProviderTypeInvalidException,
)
from lifehub.core.common.database_service import get_session
from lifehub.core.module.repository import ModuleDBClient
from lifehub.core.module.schema import Module
from lifehub.core.provider.schema import Provider
from lifehub.core.user.schema import User
from lifehub.core.user.service import (
    AUTH_ALGORITHM,
    AUTH_SECRET_KEY,
    CredentialsException,
    oauth2_scheme,
)


def yield_session():
    with get_session() as session:
        yield session


SessionDep = Annotated[Session, Depends(yield_session)]


def get_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep,
) -> User:
    try:
        payload = jwt.decode(token, AUTH_SECRET_KEY, algorithms=[AUTH_ALGORITHM])
    except JWTError:
        raise CredentialsException()

    db_client = UserDBClient(session)

    username: str = payload.get("sub")  # type: ignore

    user = db_client.get_by_username(username)
    if user is None:
        raise CredentialsException()
    return user


UserDep = Annotated[User, Depends(get_user)]


def get_provider(
    provider_id: int,
    session: SessionDep,
) -> Provider:
    provider = ProviderDBClient(session).get_by_id(provider_id)
    if not provider:
        raise ProviderDoesNotExistException(provider_id)
    return provider


ProviderDep = Annotated[Provider, Depends(get_provider)]


def get_oauth_provider(provider: ProviderDep) -> Provider:
    if provider.config.auth_type != "oauth":
        raise ProviderTypeInvalidException("OAuth")
    return provider


def get_token_provider(provider: ProviderDep) -> Provider:
    if provider.config.auth_type != "token":
        raise ProviderTypeInvalidException("Token")
    return provider


def get_basic_provider(provider: ProviderDep) -> Provider:
    if provider.config.auth_type != "basic":
        raise ProviderTypeInvalidException("Basic")
    return provider


OAuthProviderDep = Annotated[Provider, Depends(get_oauth_provider)]
TokenProviderDep = Annotated[Provider, Depends(get_token_provider)]
BasicProviderDep = Annotated[Provider, Depends(get_basic_provider)]


def get_module(module_id: int, session: SessionDep):
    module = ModuleDBClient(session).get_by_id(module_id)
    if not module:
        raise HTTPException(404, f"Module with ID {module_id} does not exist")
    return module


ModuleDep = Annotated[Module, Depends(get_module)]
