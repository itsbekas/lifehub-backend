import datetime as dt

from sqlalchemy import Session, select

from lifehub.clients.db.base import BaseDBClient
from lifehub.models.util import FetchUpdate, Module


class FetchUpdateDBClient(BaseDBClient[FetchUpdate]):
    def __init__(self, session: Session):
        super().__init__(FetchUpdate, session)

    def get(self, module: Module) -> FetchUpdate:
        stmt = select(FetchUpdate).where(FetchUpdate.module_id == module.id)
        return self.session.exec(stmt).first()

    def update(self, module: Module) -> FetchUpdate:
        fetch_update = self.get(module)
        fetch_update.last_update = dt.datetime.now()
        self.session.add(fetch_update)
        return fetch_update
