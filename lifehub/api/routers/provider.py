from typing import Annotated

from fastapi import APIRouter, Depends

from lifehub.api.exceptions.provider import (
    ProviderDoesNotExistException,
    ProviderTypeInvalidException,
)
from lifehub.api.routers.dependencies import user_is_authenticated
from lifehub.clients.db.provider import (
    OAuthProviderConfigDBClient,
    ProviderDBClient,
)
from lifehub.models.provider import Provider

router = APIRouter(
    prefix="/provider",
    tags=["provider"],
    dependencies=[Depends(user_is_authenticated)],
)


def verify_provider(provider: str):
    db_client = ProviderDBClient()
    p = db_client.get_by_name(provider)
    if not p:
        raise ProviderDoesNotExistException(provider)
    return p


VerifyProviderDep = Annotated[Provider, Depends(verify_provider)]


def verify_oauth_provider(provider: VerifyProviderDep):
    if provider.type != "oauth":
        raise ProviderTypeInvalidException("OAuth")
    return provider.name


def verify_token_provider(provider: VerifyProviderDep):
    if provider.type != "token":
        raise ProviderTypeInvalidException("Token")
    return provider.name


VerifyOAuthProviderDep = Annotated[str, Depends(verify_oauth_provider)]
VerifyTokenProviderDep = Annotated[str, Depends(verify_token_provider)]


@router.get("/{provider}/auth_url", response_model=str)
async def oauth_authorization_url(
    provider: VerifyOAuthProviderDep,
):
    db_client = OAuthProviderConfigDBClient()
    config = db_client.get_by_name(provider)
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
