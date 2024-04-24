from sqlalchemy import select

from lifehub.clients.db.base import BaseDBClient
from lifehub.models.provider import APIToken, Provider
from lifehub.models.user import User


class APITokenDBClient(BaseDBClient[APIToken]):
    def __init__(self):
        super().__init__(APIToken)

    def get(self, user: User, provider: Provider) -> APIToken | None:
        with self.session as session:
            stmt = select(APIToken).where(
                APIToken.user_id == user.id, APIToken.provider_id == provider.id
            )
            return session.exec(stmt).scalar_one_or_none()
