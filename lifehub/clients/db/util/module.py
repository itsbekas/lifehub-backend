from sqlmodel import select

from lifehub.clients.db.base import BaseDBClient
from lifehub.models.util import Module


class ModuleDBClient(BaseDBClient[Module]):
    def __init__(self):
        super().__init__(Module)

    def get_by_name(self, name: str) -> Module | None:
        with self.session as session:
            statement = select(Module).where(Module.name == name)
            result = session.exec(statement)
            return result.one_or_none()
