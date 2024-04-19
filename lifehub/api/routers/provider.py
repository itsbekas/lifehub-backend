import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from lifehub.api.exceptions.provider import (
    ProviderDoesNotExistException,
    ProviderTypeInvalidException,
)
from lifehub.api.routers.dependencies import get_user_id
from lifehub.clients.db.provider import (
    APITokenDBClient,
    OAuthProviderConfigDBClient,
    ProviderDBClient,
)
from lifehub.models.provider import APIToken

router = APIRouter(
    prefix="/provider",
    tags=["provider"],
)


def verify_provider(name: str):
    db_client = ProviderDBClient()
    provider = db_client.get_by_name(name)
    if not provider:
        raise ProviderDoesNotExistException(name)
    return provider


def verify_oauth_provider(provider: Annotated[str, Depends(verify_provider)]):
    if provider.type != "oauth":
        raise ProviderTypeInvalidException()
    return provider.name


def verify_token_provider(provider: Annotated[str, Depends(verify_provider)]):
    if provider.type != "token":
        raise ProviderTypeInvalidException()
    return provider.name


@router.get("/oauth/auth", response_model=str)
async def oauth_authorization_url(
    provider: Annotated[str, Depends(verify_oauth_provider)],
    user_id: Annotated[uuid.UUID, Depends(get_user_id)],
):
    db_client = OAuthProviderConfigDBClient()
    config = db_client.get_by_name(provider)
    return config.build_auth_url()


@router.get("/oauth/token", response_model=str)
async def oauth_token_url(
    provider: Annotated[str, Depends(verify_oauth_provider)],
    user_id: Annotated[uuid.UUID, Depends(get_user_id)],
    code: str,
):
    db_client = OAuthProviderConfigDBClient()
    config = db_client.get_by_name(provider)
    return config.build_token_url(code)


@router.post("/token", response_model=None)
async def token(
    provider: Annotated[str, Depends(verify_token_provider)],
    user_id: Annotated[uuid.UUID, Depends(get_user_id)],
    token: str,
):
    api_token = APIToken(
        provider=provider,
        token=token,
        user_id=user_id,
        created_at=None,
        expires_at=None,
    )

    db_client = APITokenDBClient()
    db_client.add(api_token)
