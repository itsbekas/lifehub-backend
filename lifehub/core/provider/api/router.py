from typing import List

from fastapi import APIRouter, Depends

from lifehub.core.provider.api.dependencies import ProviderDep, ProviderServiceDep
from lifehub.core.provider.models import ProviderWithModulesResponse
from lifehub.core.user.api.dependencies import user_is_authenticated

router = APIRouter(
    dependencies=[Depends(user_is_authenticated)],
)


@router.get("", response_model=List[ProviderWithModulesResponse])
async def get_providers(provider_service: ProviderServiceDep):
    return provider_service.get_providers_with_modules()


@router.get("/{provider_id}/oauth_url", response_model=str)
async def oauth_authorization_url(provider: ProviderDep):
    if provider.config.auth_type != "oauth":
        raise Exception("Provider does not support OAuth")

    return provider.config.build_auth_url()
