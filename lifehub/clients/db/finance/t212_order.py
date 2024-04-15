import uuid

from lifehub.clients.db.base import TimeUserBaseDBClient
from lifehub.models.finance import T212Order


class T212OrderDBClient(TimeUserBaseDBClient[T212Order]):
    def __init__(self, user_id: uuid.UUID):
        super().__init__(T212Order, user_id)
