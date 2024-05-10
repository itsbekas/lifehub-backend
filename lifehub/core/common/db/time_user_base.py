from typing import Type

from sqlalchemy import Session, select

from lifehub.clients.db.db.base import BaseModelType
from lifehub.clients.db.db.user_base import UserBaseDBClient
from lifehub.core.user.schema import User


class TimeUserBaseDBClient(UserBaseDBClient[BaseModelType]):
    def __init__(self, model: Type[BaseModelType], user: User, session: Session):
        super().__init__(model, user, session)

    def get_latest(self) -> BaseModelType | None:
        statement = (
            select(self.model)
            .where(self.model.user_id == self.user.id)
            .order_by(self.model.timestamp.desc())
            .limit(1)
        )
        result = self.session.exec(statement)
        return result.one_or_none()
