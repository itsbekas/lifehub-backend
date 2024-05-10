import datetime as dt

import requests
from fastapi import APIRouter, HTTPException
from sqlmodel import SQLModel

from lifehub.clients.api import api_clients
from lifehub.clients.db.repository.oauth_provider_config import (
    OAuthProviderConfigRepository,
)
from lifehub.clients.db.repository.provider_token import APITokenRepository
from lifehub.core.common.api.dependencies import (
    BasicProviderDep,
    OAuthProviderDep,
    ProviderDep,
    SessionDep,
    TokenProviderDep,
    UserDep,
)
from lifehub.models.provider_old.api_token import (
    APIToken,
    APITokenBasicRequest,
    APITokenTokenRequest,
)
from lifehub.models.provider_old.provider import ProviderType
from lifehub.models.util.module import Module

router = APIRouter()


class OAuthTokenRequestFailedException(HTTPException):
    def __init__(self, response: requests.Response):
        super().__init__(response.status_code, response.text)


class NoTokenException(HTTPException):
    def __init__(self):
        super().__init__(404, "No token found")


class InvalidTokenException(HTTPException):
    def __init__(self):
        super().__init__(403, "Invalid token")


class ProviderWithModules(SQLModel):
    id: int
    name: str
    type: ProviderType
    modules: list[Module]


@router.get("", response_model=list[ProviderWithModules])
async def get_user_providers(user: UserDep):
    return user.providers


@router.delete("/{provider_id}")
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
    token = APITokenRepository(session).get(user, provider)
    session.delete(token)

    session.add(user)
    session.commit()


@router.post("/{provider_id}/oauth_token")
async def oauth_token(
    provider: OAuthProviderDep,
    user: UserDep,
    session: SessionDep,
    code: str,
):
    url = OAuthProviderConfigRepository(session).get(provider.id).build_token_url(code)
    res = requests.post(url)
    if res.status_code != 200:
        raise OAuthTokenRequestFailedException(res)
    data = res.json()

    created_at: dt.datetime = dt.datetime.fromtimestamp(data["created_at"])
    expires_at: dt.datetime = created_at + dt.timedelta(seconds=data["expires_in"])

    api_token = APIToken(
        user_id=user.id,
        provider_id=provider.id,
        token=data["access_token"],
        refresh_token=data.get("refresh_token"),
        created_at=created_at,
        expires_at=expires_at,
    )
    session.add(api_token)
    user = session.merge(user)
    user.providers.append(provider)
    session.add(user)
    session.commit()


@router.post("/{provider_id}/basic_token")
async def create_basic_token(
    provider: TokenProviderDep,
    user: UserDep,
    session: SessionDep,
    req: APITokenTokenRequest,
):
    api_token = APITokenRepository(session).get(user, provider)

    if api_token is not None:
        raise HTTPException(409, "Token already exists")

    custom_url = None
    if req.custom_url is not None:
        custom_url = req.custom_url

    api_token = APIToken(
        user_id=user.id,
        provider_id=provider.id,
        custom_url=custom_url,
        token=req.token,
        created_at=None,
        expires_at=None,
    )
    user = session.merge(user)
    user.providers.append(provider)
    session.add(user)
    session.add(api_token)
    session.commit()


@router.patch("/{provider_id}/basic_token")
async def update_basic_token(
    provider: TokenProviderDep,
    user: UserDep,
    session: SessionDep,
    req: APITokenTokenRequest,
):
    api_token = APITokenRepository(session).get(user, provider)
    if api_token is None:
        raise NoTokenException()
    api_token.token = req.token
    session.add(api_token)
    session.commit()


@router.post("/{provider_id}/basic_login")
async def create_basic_login(
    provider: BasicProviderDep,
    user: UserDep,
    session: SessionDep,
    req: APITokenBasicRequest,
):
    api_token = APITokenRepository(session).get(user, provider)

    if api_token is not None:
        raise HTTPException(409, "Token already exists")

    custom_url = None
    if req.custom_url is not None:
        custom_url = req.custom_url

    api_token = APIToken(
        user_id=user.id,
        provider_id=provider.id,
        custom_url=custom_url,
        token=f"{req.username}:{req.password}",
        created_at=None,
        expires_at=None,
    )
    user = session.merge(user)
    user.providers.append(provider)
    session.add(user)
    session.add(api_token)
    session.commit()


@router.patch("/{provider_id}/basic_login")
async def update_basic_login(
    provider: BasicProviderDep,
    user: UserDep,
    session: SessionDep,
    req: APITokenBasicRequest,
):
    api_token = APITokenRepository(session).get(user, provider)
    if api_token is None:
        raise NoTokenException()
    api_token.token = f"{req.username}:{req.password}"
    session.add(api_token)
    session.commit()


@router.get("/{provider_id}/test")
async def test_user_provider_connection(provider: ProviderDep, user: UserDep):
    APIClient = api_clients.get(provider.name)
    try:
        client = APIClient(user)
    except AttributeError:
        raise NoTokenException()

    if not client.test_connection():
        raise InvalidTokenException()
