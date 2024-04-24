from sqlmodel import Session, select

from lifehub.clients.db.base import BaseDBClient
from lifehub.models.user import User


class UserDBClient(BaseDBClient[User]):
    def __init__(self, session: Session):
        super().__init__(User, session)

    def get_by_username(self, username: str) -> User | None:
        query = select(User).where(User.username == username)
        return self.session.exec(query).one_or_none()
