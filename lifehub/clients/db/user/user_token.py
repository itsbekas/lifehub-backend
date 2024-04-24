from sqlmodel import Session

from lifehub.clients.db.base import UserBaseDBClient
from lifehub.models.user import User, UserToken


class UserTokenDBClient(UserBaseDBClient[UserToken]):
    def __init__(self, user: User, session: Session):
        super().__init__(UserToken, user, session)
