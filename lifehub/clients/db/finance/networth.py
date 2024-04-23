from lifehub.clients.db.base import TimeUserBaseDBClient
from lifehub.models.finance import Networth
from lifehub.models.user import User


class NetworthDBClient(TimeUserBaseDBClient[Networth]):
    def __init__(self, user: User):
        super().__init__(Networth, user)
