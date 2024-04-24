from sqlmodel import select

from lifehub.clients.db.base import BaseDBClient
from lifehub.models.provider import Provider


class ProviderDBClient(BaseDBClient[Provider]):
    def __init__(self):
        super().__init__(Provider)

    def get_by_name(self, name: str) -> Provider | None:
        with self.session as session:
            stmt = select(Provider).where(Provider.name == name)
            return session.exec(stmt).one_or_none()
