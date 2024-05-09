from sqlmodel import Session

from lifehub.clients.db.base import TimeUserBaseDBClient
from lifehub.models.finance import T212Transaction
from lifehub.models.user_old import User


class T212TransactionDBClient(TimeUserBaseDBClient[T212Transaction]):
    def __init__(self, user: User, session: Session):
        super().__init__(T212Transaction, user, session)
