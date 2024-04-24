from sqlmodel import Session, select

from lifehub.clients.db.base import BaseDBClient
from lifehub.models.util import ModuleProvider


class ModuleProviderDBClient(BaseDBClient[ModuleProvider]):
    def __init__(self, module: str, session: Session):
        super().__init__(ModuleProvider, session)
        self.module = module

    def get_providers(self):
        statement = select(ModuleProvider).where(ModuleProvider.module == self.module)
        result = self.session.exec(statement)
        return result.all()
