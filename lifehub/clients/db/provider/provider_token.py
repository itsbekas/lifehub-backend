from sqlmodel import Session, select

from lifehub.clients.db.base import BaseDBClient
from lifehub.core.provider.models import Provider, ProviderToken
from lifehub.core.user.models import User


class ProviderTokenDBClient(BaseDBClient[ProviderToken]):
    def __init__(self, session: Session):
        super().__init__(ProviderToken, session)

    def get(self, user: User, provider: Provider) -> ProviderToken | None:
        stmt = select(ProviderToken).where(
            ProviderToken.user_id == user.id, ProviderToken.provider_id == provider.id
        )
        return self.session.exec(stmt).one_or_none()
