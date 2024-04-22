from os import getenv

from lifehub.clients.db.service import DatabaseService
from lifehub.models.provider import OAuthProviderConfig, Provider, ProviderType


def oauth_redirect_uri(provider_name: str) -> str:
    return getenv("REDIRECT_URI_BASE") + f"/provider/{provider_name}/callback"


def setup_providers():
    db = DatabaseService()

    providers = {
        "trading212": Provider(name="trading212", type=ProviderType.token),
        "ynab": Provider(name="ynab", type=ProviderType.oauth),
        "qbittorrent": Provider(name="qbittorrent", type=ProviderType.basic),
    }

    with db.get_session() as session:
        for name in providers:
            session.add(providers[name])
        session.commit()
        for name in providers:
            session.refresh(providers[name])

    oauth_provider_configs = {
        "ynab": OAuthProviderConfig(
            provider_id=providers["ynab"].id,
            auth_url="https://app.ynab.com/oauth/authorize",
            token_url="https://app.ynab.com/oauth/token",
            client_id=getenv("YNAB_CLIENT_ID"),
            client_secret=getenv("YNAB_CLIENT_SECRET"),
            scope="read-only",
            redirect_uri=oauth_redirect_uri("ynab"),
        ),
    }

    with db.get_session() as session:
        for name in oauth_provider_configs:
            session.add(oauth_provider_configs[name])
        session.commit()
