from sqlmodel import select

from lifehub.clients.db.base import BaseDBClient
from lifehub.models.util import ModuleProvider


class ModuleProviderDBClient(BaseDBClient[ModuleProvider]):
    def __init__(self, module: str):
        super().__init__(ModuleProvider)
        self.module = module

    def get_providers(self):
        with self.session as session:
            statement = select(ModuleProvider).where(
                ModuleProvider.module == self.module
            )
            result = session.exec(statement)
            return result.all()
