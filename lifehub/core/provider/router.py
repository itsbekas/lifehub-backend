from fastapi import APIRouter, Depends

from lifehub.clients.db.repository import (
    OAuthProviderConfigRepository,
    ProviderRepository,
)
from lifehub.core.provider.schema import Provider
from lifehub.core.user.api.dependencies import OAuthProviderDep, SessionDep, get_user

router = APIRouter(
    dependencies=[Depends(get_user)],
)


@router.get("", response_model=list[Provider])
async def get_providers(session: SessionDep):
    return ProviderRepository(session).get_all()


@router.get("/{provider_id}/oauth_url", response_model=str)
async def oauth_authorization_url(
    provider: OAuthProviderDep,
    session: SessionDep,
):
    db_client = OAuthProviderConfigRepository(session)
    config = db_client.get(provider.id)

    if config is None:
        raise Exception("Provider is not configured")

    return config.build_auth_url()
