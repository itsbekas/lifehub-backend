from sqlalchemy import Session, select

from lifehub.clients.db.base import BaseDBClient
from lifehub.models.util import Module


class ModuleDBClient(BaseDBClient[Module]):
    def __init__(self, session: Session):
        super().__init__(Module, session=session)

    def get_by_id(self, id: int, retrieve_users: bool = False) -> Module | None:
        query = select(Module).filter(Module.id == id)
        module = self.session.exec(query).first()
        if retrieve_users:
            module.users
        return module

    def get_by_name(self, name: str, retrieve_users: bool = False) -> Module | None:
        query = select(Module).filter(Module.name == name)
        module = self.session.exec(query).first()
        if retrieve_users:
            module.users
        return module
