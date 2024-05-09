from sqlmodel import Session

from lifehub.clients.db.base import TimeUserBaseDBClient
from lifehub.models.user_old import User
from lifehub.modules.finance.schema import T212Order


class T212OrderDBClient(TimeUserBaseDBClient[T212Order]):
    def __init__(self, user: User, session: Session):
        super().__init__(T212Order, user, session)
