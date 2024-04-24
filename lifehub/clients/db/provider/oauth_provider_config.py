from sqlmodel import Session, select

from lifehub.clients.db.base import BaseDBClient
from lifehub.models.provider import OAuthProviderConfig


class OAuthProviderConfigDBClient(BaseDBClient[OAuthProviderConfig]):
    def __init__(self, session: Session):
        super().__init__(OAuthProviderConfig, session)

    def get(self, provider_id: int) -> OAuthProviderConfig | None:
        query = select(OAuthProviderConfig).where(
            OAuthProviderConfig.provider_id == provider_id
        )
        return self.session.exec(query).one_or_none()
