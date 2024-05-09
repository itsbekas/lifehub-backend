from os import getenv

from lifehub.clients.db.service import get_session
from lifehub.models.module import Module
from lifehub.models.provider import (
    BasicProviderConfig,
    OAuthProviderConfig,
    Provider,
    TokenProviderConfig,
)


def init_setup_data():
    provider_configs = {
        "trading212": {
            "auth_type": "token",
        },
        "ynab": {
            "auth_type": "oauth",
            "auth_url": "https://app.ynab.com/oauth/authorize",
            "token_url": "https://app.ynab.com/oauth/token",
            "client_id": getenv("YNAB_CLIENT_ID"),
            "client_secret": getenv("YNAB_CLIENT_SECRET"),
            "scope": "read-only",
        },
        "qbittorrent": {
            "auth_type": "basic",
            "allow_custom_url": True,
        },
    }

    module_providers = {
        "networth": ["trading212", "ynab"],
        "t212history": ["trading212"],
        "server": ["qbittorrent"],
    }

    return provider_configs, module_providers


def setup_providers():
    provider_configs, module_providers = init_setup_data()

    session = get_session()
    providers_dict = {}

    for name in provider_configs:
        provider = Provider(name=name)
        session.add(provider)
        session.flush()  # Ensure the provider ID is available
        providers_dict[name] = provider

        config = provider_configs[name]
        if config["auth_type"] == "oauth":
            provider_config = OAuthProviderConfig(
                provider_id=provider.id,
                auth_url=config["auth_url"],
                allow_custom_url=config.get("allow_custom_url", False),
                token_url=config["token_url"],
                client_id=config["client_id"],
                client_secret=config["client_secret"],
                scope=config["scope"],
            )
        elif config["auth_type"] == "token":
            provider_config = TokenProviderConfig(
                provider_id=provider.id,
                allow_custom_url=config.get("allow_custom_url", False),
            )
        elif config["auth_type"] == "basic":
            provider_config = BasicProviderConfig(
                provider_id=provider.id,
                allow_custom_url=config.get("allow_custom_url", False),
            )

        provider.config = provider_config
        session.add(provider_config)

    session.commit()

    modules = []
    for module_name, provider_names in module_providers.items():
        module_providers_list = [
            providers_dict[provider_name] for provider_name in provider_names
        ]
        module = Module(name=module_name, providers=module_providers_list)
        modules.append(module)
        session.add(module)

    session.commit()
