from lifehub.clients.db.base import BaseDBClient
from lifehub.models.util import FetchUpdate


class FetchUpdateDBClient(BaseDBClient[FetchUpdate]):
    def __init__(self):
        super().__init__(FetchUpdate)
