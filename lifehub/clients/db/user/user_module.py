from sqlmodel import Session

from lifehub.clients.db.base import UserBaseDBClient
from lifehub.models.user import User, UserModule


class UserModuleDBClient(UserBaseDBClient[UserModule]):
    def __init__(self, user: User, session: Session):
        super().__init__(UserModule, user, session)
