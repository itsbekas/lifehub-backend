from lifehub.models.user import User
from lifehub.clients.db.base import BaseDBClient
from sqlmodel import select

class UserDBClient(BaseDBClient[User]):
    def __init__(self):
        super().__init__(User)
    
    def get_by_username(self, username: str) -> User | None:
        with self.session as session:
            query = select(User).where(User.username == username)
            return session.exec(query).one_or_none()
