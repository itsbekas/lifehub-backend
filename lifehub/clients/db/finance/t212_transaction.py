import uuid

from lifehub.clients.db.base import TimeUserBaseDBClient
from lifehub.models.finance import T212Transaction


class T212TransactionDBClient(TimeUserBaseDBClient[T212Transaction]):
    def __init__(self, user_id: uuid.UUID):
        super().__init__(T212Transaction, user_id)
