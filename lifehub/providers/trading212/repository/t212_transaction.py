from sqlalchemy import Session

from lifehub.core.common.repository.time_user_base import TimeUserBaseRepository
from lifehub.core.user.schema import User
from lifehub.providers.trading212.schema import T212Transaction


class T212TransactionRepository(TimeUserBaseRepository[T212Transaction]):
    def __init__(self, user: User, session: Session):
        super().__init__(T212Transaction, user, session)
