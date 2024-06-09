from sqlalchemy.orm import Session

from lifehub.core.common.database_service import get_session
from lifehub.core.user.schema import User


class BaseUserService:
    def __init__(self, user: User) -> None:
        self.session: Session = get_session()
        self.user = self.session.merge(user)
