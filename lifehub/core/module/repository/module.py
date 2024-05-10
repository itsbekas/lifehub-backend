from sqlalchemy import select
from sqlalchemy.orm import Session

from lifehub.core.common.repository.base import BaseRepository
from lifehub.core.module.schema import Module


class ModuleRepository(BaseRepository[Module]):
    def __init__(self, session: Session):
        super().__init__(Module, session=session)

    def get_by_id(self, id: int, retrieve_users: bool = False) -> Module | None:
        query = select(Module).filter(Module.id == id)
        module = self.session.execute(query).scalar_one_or_none()
        if module is not None and retrieve_users:
            module.users
        return module

    def get_by_name(self, name: str, retrieve_users: bool = False) -> Module | None:
        query = select(Module).filter(Module.name == name)
        module = self.session.execute(query).scalar_one_or_none()
        if module is not None and retrieve_users:
            module.users
        return module
