from sqlalchemy import Session

from lifehub.clients.db.base import TimeUserBaseDBClient
from lifehub.core.user.schema import User
from lifehub.providers.trading212.schema import T212Transaction


class T212TransactionDBClient(TimeUserBaseDBClient[T212Transaction]):
    def __init__(self, user: User, session: Session):
        super().__init__(T212Transaction, user, session)
