import uuid

from lifehub.clients.db.time_user_base import TimeUserBaseDBClient
from lifehub.models.finance import Networth


class NetworthDBClient(TimeUserBaseDBClient[Networth]):
    def __init__(self, user_id: uuid.UUID):
        super().__init__(Networth, user_id)
