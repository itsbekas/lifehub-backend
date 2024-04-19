from os import getenv

from lifehub.clients.db.provider import OAuthProviderConfigDBClient, ProviderDBClient
from lifehub.models.provider import OAuthProviderConfig, Provider


def setup_providers():
    providers = [
        Provider(
            name="trading212",
            type="token",
        ),
        Provider(
            name="ynab",
            type="oauth",
        ),
        Provider(
            name="qbittorrent",
            type="basic",
        ),
    ]

    oauth_provider_configs = [
        OAuthProviderConfig(
            name="ynab",
            auth_url="https://app.ynab.com/oauth/authorize",
            token_url="https://app.ynab.com/oauth/token",
            client_id=getenv("YNAB_CLIENT_ID"),
            client_secret=getenv("YNAB_CLIENT_SECRET"),
            scope="read-only",
        ),
    ]

    db_client = ProviderDBClient()
    for provider in providers:
        db_client.add(provider)

    db_client = OAuthProviderConfigDBClient()
    for config in oauth_provider_configs:
        config.redirect_uri = (
            getenv("REDIRECT_URI_BASE") + f"/provider/{config.name}/callback"
        )
        db_client.add(config)
