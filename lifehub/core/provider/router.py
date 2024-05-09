from fastapi import APIRouter, Depends

from lifehub.clients.db.provider import (
    OAuthProviderConfigDBClient,
    ProviderDBClient,
)
from lifehub.core.api_dependencies import OAuthProviderDep, SessionDep, get_user
from lifehub.core.provider.schema import Provider

router = APIRouter(
    dependencies=[Depends(get_user)],
)


@router.get("", response_model=list[Provider])
async def get_providers(session: SessionDep):
    return ProviderDBClient(session).get_all()


@router.get("/{provider_id}/oauth_url", response_model=str)
async def oauth_authorization_url(
    provider: OAuthProviderDep,
    session: SessionDep,
):
    db_client = OAuthProviderConfigDBClient(session)
    config = db_client.get(provider.id)
    return config.build_auth_url()
