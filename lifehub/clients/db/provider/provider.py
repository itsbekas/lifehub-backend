from sqlmodel import Session, select

from lifehub.clients.db.base import BaseDBClient
from lifehub.models.provider import Provider


class ProviderDBClient(BaseDBClient[Provider]):
    def __init__(self, session: Session):
        super().__init__(Provider, session)

    def get_by_name(self, name: str) -> Provider | None:
        stmt = select(Provider).where(Provider.name == name)
        return self.session.exec(stmt).one_or_none()
