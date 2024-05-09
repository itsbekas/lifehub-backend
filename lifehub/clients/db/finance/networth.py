from sqlmodel import Session

from lifehub.clients.db.base import TimeUserBaseDBClient
from lifehub.core.user.models import User
from lifehub.modules.finance.models import Networth


class NetworthDBClient(TimeUserBaseDBClient[Networth]):
    def __init__(self, user: User, session: Session):
        super().__init__(Networth, user, session)
