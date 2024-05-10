from sqlalchemy import Session

from lifehub.clients.db.base import TimeUserBaseDBClient
from lifehub.core.user.schema import User
from lifehub.providers.trading212.schema import T212Order


class T212OrderDBClient(TimeUserBaseDBClient[T212Order]):
    def __init__(self, user: User, session: Session):
        super().__init__(T212Order, user, session)
