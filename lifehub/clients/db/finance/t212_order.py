from sqlmodel import Session

from lifehub.clients.db.base import TimeUserBaseDBClient
from lifehub.models.finance import T212Order
from lifehub.models.user_old import User


class T212OrderDBClient(TimeUserBaseDBClient[T212Order]):
    def __init__(self, user: User, session: Session):
        super().__init__(T212Order, user, session)
