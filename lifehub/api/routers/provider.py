import datetime as dt
from typing import Annotated

import requests
from fastapi import APIRouter, Depends, Form, HTTPException

from lifehub.api.exceptions import (
    ProviderDoesNotExistException,
    ProviderTypeInvalidException,
)
from lifehub.api.routers.dependencies import SessionDep, UserDep, get_user
from lifehub.clients.api import api_clients
from lifehub.clients.db.provider import (
    APITokenDBClient,
    OAuthProviderConfigDBClient,
    ProviderDBClient,
)
from lifehub.models.provider import APIToken, Provider

router = APIRouter(
    dependencies=[Depends(get_user)],
)


class OAuthTokenRequestFailedException(HTTPException):
    def __init__(self, response: requests.Response):
        super().__init__(response.status_code, response.text)


class InvalidTokenException(HTTPException):
    def __init__(self):
        super().__init__(401, "Invalid token")


class NoTokenException(HTTPException):
    def __init__(self):
        super().__init__(404, "No token found")


def verify_provider(
    provider_name: str,
    session: SessionDep,
) -> Provider:
    provider = ProviderDBClient(session).get_by_name(provider_name)
    if not provider:
        raise ProviderDoesNotExistException(provider_name)
    return provider


VerifyProviderDep = Annotated[Provider, Depends(verify_provider)]


def verify_oauth_provider(provider: VerifyProviderDep) -> Provider:
    if provider.type != "oauth":
        raise ProviderTypeInvalidException("OAuth")
    return provider


def verify_token_provider(provider: VerifyProviderDep) -> Provider:
    if provider.type != "token":
        raise ProviderTypeInvalidException("Token")
    return provider


def verify_basic_provider(provider: VerifyProviderDep) -> Provider:
    if provider.type != "basic":
        raise ProviderTypeInvalidException("Basic")
    return provider


VerifyOAuthProviderDep = Annotated[str, Depends(verify_oauth_provider)]
VerifyTokenProviderDep = Annotated[str, Depends(verify_token_provider)]
VerifyBasicProviderDep = Annotated[str, Depends(verify_basic_provider)]


@router.get("/{provider_name}/oauth_url", response_model=str)
async def oauth_authorization_url(
    provider: VerifyOAuthProviderDep,
    session: SessionDep,
):
    db_client = OAuthProviderConfigDBClient(session)
    config = db_client.get(provider.id)
    return config.build_auth_url()


@router.get("/{provider_name}/oauth_token")
async def oauth_token(
    provider: VerifyOAuthProviderDep,
    user: UserDep,
    session: SessionDep,
    code: str,
):
    url = OAuthProviderConfigDBClient(session).get(provider.id).build_token_url(code)
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


@router.post("/{provider_name}/token")
async def add_token(
    provider: VerifyTokenProviderDep,
    user: UserDep,
    session: SessionDep,
    token: str,
):
    api_token = APIToken(
        user_id=user.id,
        provider_id=provider.id,
        token=token,
        created_at=None,
        expires_at=None,
    )
    session.add(api_token)
    user = session.merge(user)
    user.providers.append(provider)
    session.add(user)
    session.commit()


@router.put("/{provider_name}/token")
async def modify_token(
    provider: VerifyTokenProviderDep,
    user: UserDep,
    session: SessionDep,
    token: str,
):
    api_token = APITokenDBClient(session).get(user, provider)
    if api_token is None:
        raise NoTokenException()
    api_token.token = token
    api_token.created_at = dt.datetime.now()
    session.add(api_token)
    session.commit()


@router.delete("/{provider_name}/token")
async def remove_token(
    provider: VerifyTokenProviderDep,
    user: UserDep,
    session: SessionDep,
):
    api_token = APITokenDBClient(session).get(user, provider)
    session.delete(api_token)
    session.commit()


@router.post("/{provider_name}/login")
async def basic_login(
    provider: VerifyBasicProviderDep,
    user: UserDep,
    session: SessionDep,
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    url: Annotated[str, Form()],
):
    api_token = APIToken(
        user_id=user.id,
        provider_id=provider.id,
        token=f"{username}:{password};{url}",
        created_at=None,
        expires_at=None,
    )
    session.add(api_token)
    user = session.merge(user)
    user.providers.append(provider)
    session.add(user)
    session.commit()


@router.get("/{provider_name}/test")
async def test_connection(provider: VerifyProviderDep, user: UserDep):
    APIClient = api_clients.get(provider.name)
    try:
        client = APIClient(user)
    except AttributeError:
        raise NoTokenException()

    if not client.test_connection():
        raise InvalidTokenException()
