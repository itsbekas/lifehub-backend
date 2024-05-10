from sqlmodel import Session

from lifehub.clients.db.base import TimeUserBaseDBClient
from lifehub.models.user_old import User
from lifehub.providers.ynab.schema import T212Transaction


class T212TransactionDBClient(TimeUserBaseDBClient[T212Transaction]):
    def __init__(self, user: User, session: Session):
        super().__init__(T212Transaction, user, session)
