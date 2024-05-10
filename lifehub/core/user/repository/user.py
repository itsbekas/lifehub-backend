from sqlalchemy import Session, select

from lifehub.core.common.repository.base import BaseRepository
from lifehub.core.provider.schema import Provider
from lifehub.core.user.schema import User


class UserRepository(BaseRepository[User]):
    def __init__(self, session: Session):
        super().__init__(User, session)

    def get_by_username(self, username: str) -> User | None:
        query = select(User).where(User.username == username)
        return self.session.exec(query).one_or_none()

    def get_user_providers(self, user: User) -> list[Provider] | None:
        return user.providers
