from typing import Type

from sqlmodel import Session, select

from lifehub.clients.db.base.base import BaseModel
from lifehub.clients.db.base.user_base import UserBaseDBClient
from lifehub.models.user import User


class TimeUserBaseDBClient(UserBaseDBClient[BaseModel]):
    def __init__(self, model: Type[BaseModel], user: User, session: Session):
        super().__init__(model, user, session)

    def get_latest(self) -> BaseModel:
        statement = (
            select(self.model)
            .where(self.model.user_id == self.user.id)
            .order_by(self.model.timestamp.desc())
            .limit(1)
        )
        result = self.session.exec(statement)
        return result.one_or_none()
