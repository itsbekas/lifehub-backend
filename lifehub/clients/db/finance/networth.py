from sqlalchemy import Session

from lifehub.clients.db.base import TimeUserBaseDBClient
from lifehub.core.user.schema import User
from lifehub.providers.ynab.schema import Networth


class NetworthDBClient(TimeUserBaseDBClient[Networth]):
    def __init__(self, user: User, session: Session):
        super().__init__(Networth, user, session)
