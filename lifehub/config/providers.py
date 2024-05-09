from os import getenv

from lifehub.clients.db.service import get_session
from lifehub.models.provider_old import Provider, ProviderType
from lifehub.models.provider_old.provider_config import (
    BasicProviderConfig,
    OAuthProviderConfig,
    TokenProviderConfig,
)
from lifehub.models.util import FetchUpdate, Module


def setup_providers():
    providers = {
        "trading212": Provider(name="trading212", type=ProviderType.token),
        "ynab": Provider(name="ynab", type=ProviderType.oauth),
        "qbittorrent": Provider(name="qbittorrent", type=ProviderType.basic),
    }

    with get_session() as session:
        for name in providers:
            session.add(providers[name])
        session.commit()
        for name in providers:
            session.refresh(providers[name])

    oauth_provider_configs = {
        "trading212": TokenProviderConfig(provider_id=providers["trading212"].id),
        "ynab": OAuthProviderConfig(
            provider_id=providers["ynab"].id,
            auth_url="https://app.ynab.com/oauth/authorize",
            token_url="https://app.ynab.com/oauth/token",
            client_id=getenv("YNAB_CLIENT_ID"),
            client_secret=getenv("YNAB_CLIENT_SECRET"),
            scope="read-only",
        ),
        "qbittorrent": BasicProviderConfig(
            provider_id=providers["qbittorrent"].id,
            allow_custom_url=True,
        ),
    }

    with get_session() as session:
        for name in oauth_provider_configs:
            session.add(oauth_provider_configs[name])
        session.commit()

    modules = {
        "networth": Module(
            name="networth",
            providers=[providers["trading212"], providers["ynab"]],
            users=[],
        ),
        "t212history": Module(
            name="t212history",
            providers=[providers["trading212"]],
            users=[],
        ),
        "server": Module(
            name="server",
            providers=[providers["qbittorrent"]],
            users=[],
        ),
    }

    with get_session() as session:
        for name in modules:
            session.add(modules[name])
        session.commit()
        for name in modules:
            session.refresh(modules[name])

    fetch_updates = {
        "networth": FetchUpdate(module_id=modules["networth"].id),
        "server": FetchUpdate(module_id=modules["server"].id),
        "t212history": FetchUpdate(module_id=modules["t212history"].id),
    }

    with get_session() as session:
        for name in fetch_updates:
            session.add(fetch_updates[name])
        session.commit()
