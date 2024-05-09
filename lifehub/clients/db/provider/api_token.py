from sqlmodel import Session, select

from lifehub.clients.db.base import BaseDBClient
from lifehub.models.provider_old import APIToken, Provider
from lifehub.models.user_old import User


class APITokenDBClient(BaseDBClient[APIToken]):
    def __init__(self, session: Session):
        super().__init__(APIToken, session)

    def get(self, user: User, provider: Provider) -> APIToken | None:
        stmt = select(APIToken).where(
            APIToken.user_id == user.id, APIToken.provider_id == provider.id
        )
        return self.session.exec(stmt).one_or_none()
