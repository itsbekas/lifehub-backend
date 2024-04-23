import datetime as dt
from typing import Annotated

import requests
from fastapi import APIRouter, Depends, Form, HTTPException
from sqlmodel import Session

from lifehub.api.exceptions.provider import (
    ProviderDoesNotExistException,
    ProviderTypeInvalidException,
)
from lifehub.api.routers.dependencies import get_session, get_user
from lifehub.clients.db.provider import (
    OAuthProviderConfigDBClient,
    ProviderDBClient,
)
from lifehub.models.provider import APIToken, Provider
from lifehub.models.user import User

router = APIRouter(
    prefix="/provider",
    tags=["provider"],
    dependencies=[Depends(get_user)],
)


class OAuthTokenRequestFailedException(HTTPException):
    def __init__(self, response: requests.Response):
        super().__init__(response.status_code, response.text)


def verify_provider(provider: str) -> Provider:
    db_client = ProviderDBClient()
    p = db_client.get_by_name(provider)
    if not p:
        raise ProviderDoesNotExistException(provider)
    return p


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


@router.get("/{provider}/oauth_url", response_model=str)
async def oauth_authorization_url(
    provider: VerifyOAuthProviderDep,
):
    db_client = OAuthProviderConfigDBClient()
    config = db_client.get(provider.id)
    return config.build_auth_url()


@router.get("/{provider}/oauth_token")
async def oauth_token(
    provider: VerifyOAuthProviderDep,
    user: Annotated[User, Depends(get_user)],
    session: Annotated[Session, Depends(get_session)],
    code: str,
):
    db_client = OAuthProviderConfigDBClient()
    config = db_client.get(provider.id)
    url = config.build_token_url(code)
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


@router.post("/{provider}/token")
async def token_login(
    provider: VerifyTokenProviderDep,
    user: Annotated[User, Depends(get_user)],
    session: Annotated[Session, Depends(get_session)],
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


@router.post("/{provider}/login")
async def basic_login(
    provider: VerifyBasicProviderDep,
    user: Annotated[User, Depends(get_user)],
    session: Annotated[Session, Depends(get_session)],
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    url: Annotated[str, Form()],
):
    api_token = APIToken(
        user_id=user.id,
        provider_id=provider.id,
        token=f"{username}:{password}:{url}",
        created_at=None,
        expires_at=None,
    )
    session.add(api_token)
    user = session.merge(user)
    user.providers.append(provider)
    session.add(user)
    session.commit()
