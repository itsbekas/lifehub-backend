from sqlmodel import select

from lifehub.clients.db.base import BaseDBClient
from lifehub.models.util import Module


class ModuleDBClient(BaseDBClient[Module]):
    def __init__(self):
        super().__init__(Module)

    def get_by_name(self, name: str, retrieve_users: bool = False) -> Module | None:
        with self.session as session:
            query = select(Module).filter(Module.name == name)
            module = session.exec(query).first()
            if retrieve_users:
                module.users
            return module
