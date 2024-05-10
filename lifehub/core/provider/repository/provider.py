from sqlalchemy import Session, select

from lifehub.clients.db.db import BaseDBClient
from lifehub.core.provider.schema import Provider


class ProviderDBClient(BaseDBClient[Provider]):
    def __init__(self, session: Session):
        super().__init__(Provider, session)

    def get_by_id(self, id: int) -> Provider | None:
        stmt = select(Provider).where(Provider.id == id)
        return self.session.exec(stmt).one_or_none()

    def get_by_name(self, name: str) -> Provider | None:
        stmt = select(Provider).where(Provider.name == name)
        return self.session.exec(stmt).one_or_none()
