from sqlmodel import select

from lifehub.clients.db.base import BaseDBClient
from lifehub.models.provider import OAuthProviderConfig


class OAuthProviderConfigDBClient(BaseDBClient[OAuthProviderConfig]):
    def __init__(self):
        super().__init__(OAuthProviderConfig)

    def get_by_name(self, name: str) -> OAuthProviderConfig | None:
        with self.session as session:
            query = select(OAuthProviderConfig).where(OAuthProviderConfig.name == name)
            return session.exec(query).one_or_none()
