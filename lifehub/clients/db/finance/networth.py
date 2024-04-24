from sqlmodel import Session

from lifehub.clients.db.base import TimeUserBaseDBClient
from lifehub.models.finance import Networth
from lifehub.models.user import User


class NetworthDBClient(TimeUserBaseDBClient[Networth]):
    def __init__(self, user: User, session: Session):
        super().__init__(Networth, user, session)
