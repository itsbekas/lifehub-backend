from typing import Annotated

from fastapi import APIRouter, Depends, Form

from lifehub.api.exceptions.provider import (
    ProviderDoesNotExistException,
    ProviderTypeInvalidException,
)
from lifehub.api.routers.dependencies import get_user, user_is_authenticated
from lifehub.clients.db.provider import (
    APITokenDBClient,
    OAuthProviderConfigDBClient,
    ProviderDBClient,
)
from lifehub.models.provider import APIToken, Provider
from lifehub.models.user import User

router = APIRouter(
    prefix="/provider",
    tags=["provider"],
    dependencies=[Depends(user_is_authenticated)],
)


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


@router.get("/{provider}/auth_url", response_model=str)
async def oauth_authorization_url(
    provider: VerifyOAuthProviderDep,
):
    db_client = OAuthProviderConfigDBClient()
    config = db_client.get(provider.id)
    return config.build_auth_url()


@router.get(
    "/{provider}/token_url",
    dependencies=[Depends(verify_oauth_provider)],
    response_model=str,
)
async def oauth_token_url(
    provider: VerifyOAuthProviderDep,
    code: str,
):
    db_client = OAuthProviderConfigDBClient()
    config = db_client.get_by_name(provider)
    return config.build_token_url(code)


@router.get("/{provider}/login")
async def basic_login(
    provider: VerifyBasicProviderDep,
    user: Annotated[User, Depends(get_user)],
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    url: Annotated[str, Form()],
):
    db_client = APITokenDBClient()
    api_token = APIToken(
        user_id=user.id,
        provider_id=provider.id,
        token=f"{username}:{password}:{url}",
        created_at=None,
        expires_at=None,
    )
    db_client.add(api_token)
