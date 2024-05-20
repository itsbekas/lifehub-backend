from typing import Annotated

from fastapi import Depends, HTTPException

from lifehub.core.provider.schema import Provider
from lifehub.core.provider.service.provider import ProviderService

ProviderServiceDep = Annotated[ProviderService, Depends(ProviderService)]


def get_provider(
    provider_id: int,
    provider_service: ProviderServiceDep,
) -> Provider:
    provider = provider_service.get_provider_by_id(provider_id)

    if provider is None:
        raise HTTPException(404, "Provider not found")

    return provider


ProviderDep = Annotated[Provider, Depends(get_provider)]


def get_oauth_provider(
    provider: ProviderDep,
) -> Provider:
    if provider.config.auth_type != "oauth":
        raise HTTPException(404, "Provider must be an OAuth provider")

    return provider


def get_token_provider(
    provider: ProviderDep,
) -> Provider:
    if provider.config.auth_type != "token":
        raise HTTPException(404, "Provider must be a token provider")

    return provider


def get_basic_provider(
    provider: ProviderDep,
) -> Provider:
    if provider.config.auth_type != "basic":
        raise HTTPException(404, "Provider must be a basic login provider")

    return provider


OAuthProviderDep = Annotated[Provider, Depends(get_oauth_provider)]
TokenProviderDep = Annotated[Provider, Depends(get_token_provider)]
BasicProviderDep = Annotated[Provider, Depends(get_basic_provider)]
