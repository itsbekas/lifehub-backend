import datetime as dt

from sqlmodel import select

from lifehub.clients.db.base import BaseDBClient
from lifehub.models.util import FetchUpdate


class FetchUpdateDBClient(BaseDBClient[FetchUpdate]):
    def __init__(self):
        super().__init__(FetchUpdate)

    def get(self, module_id: int) -> FetchUpdate:
        stmt = select(FetchUpdate).where(FetchUpdate.id == module_id)
        return self.session.exec(stmt).first()

    def update(self, module_id: int) -> FetchUpdate:
        fetch_update = self.get(module_id)
        fetch_update.last_update = dt.datetime.now()
        self.session.add(fetch_update)
        return fetch_update
