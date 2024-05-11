import datetime as dt

import requests
from fastapi import APIRouter, Depends

from lifehub.core.provider.api.dependencies import (
    BasicProviderDep,
    OAuthProviderDep,
    ProviderDep,
    TokenProviderDep,
)
from lifehub.core.provider.models import (
    ProviderResponse,
    ProviderTokenBasicRequest,
    ProviderTokenTokenRequest,
)
from lifehub.core.user.api.dependencies import (
    UserDep,
    UserServiceDep,
    user_is_authenticated,
)
from lifehub.core.user.api.user_providers.exceptions import (
    OAuthTokenRequestFailedException,
)

router = APIRouter(
    dependencies=[Depends(user_is_authenticated)],
)


@router.get("", response_model=list[ProviderResponse])
async def get_user_providers(user: UserDep, user_service: UserServiceDep):
    return user_service.get_user_providers(user)


@router.delete("/{provider_id}")
async def remove_user_provider(
    user: UserDep,
    provider: ProviderDep,
    user_service: UserServiceDep,
):
    user_service.remove_provider_from_user(user, provider)


@router.post("/{provider_id}/oauth_token")
async def oauth_token(
    provider: OAuthProviderDep,
    user: UserDep,
    user_service: UserServiceDep,
    code: str,
):
    url = provider.config.build_token_url(code)
    res = requests.post(url)
    if res.status_code != 200:
        raise OAuthTokenRequestFailedException(res)
    data = res.json()

    created_at: dt.datetime = dt.datetime.fromtimestamp(data["created_at"])
    expires_at: dt.datetime = created_at + dt.timedelta(seconds=data["expires_in"])

    user_service.add_provider_token_to_user(
        user,
        provider,
        data["access_token"],
        data["refresh_token"],
        created_at,
        expires_at,
    )


@router.post("/{provider_id}/basic_token")
async def create_basic_token(
    provider: TokenProviderDep,
    user: UserDep,
    user_service: UserServiceDep,
    req: ProviderTokenTokenRequest,
):
    user_service.add_provider_token_to_user(user, provider, req.token, None, None, None)


@router.patch("/{provider_id}/basic_token")
async def update_basic_token(
    provider: TokenProviderDep,
    user: UserDep,
    user_service: UserServiceDep,
    req: ProviderTokenTokenRequest,
):
    user_service.update_provider_token(user, provider, req.token)


@router.post("/{provider_id}/basic_login")
async def create_basic_login(
    provider: BasicProviderDep,
    user: UserDep,
    user_service: UserServiceDep,
    req: ProviderTokenBasicRequest,
):
    user_service.add_provider_token_to_user(
        user, provider, f"{req.username}:{req.password}", None, None, None
    )


@router.patch("/{provider_id}/basic_login")
async def update_basic_login(
    provider: BasicProviderDep,
    user: UserDep,
    user_service: UserServiceDep,
    req: ProviderTokenBasicRequest,
):
    user_service.update_provider_token(user, provider, f"{req.username}:{req.password}")


# @router.get("/{provider_id}/test")
# async def test_user_provider_connection(provider: ProviderDep, user: UserDep):
#     APIClient = api_clients.get(provider.name)
#     try:
#         client = APIClient(user)
#     except AttributeError:
#         raise NoTokenException()

#     if not client.test_connection():
#         raise InvalidTokenException()
