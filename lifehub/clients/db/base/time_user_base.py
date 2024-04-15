import uuid
from typing import Type

from sqlmodel import select

from lifehub.clients.db.base import BaseModel, UserBaseDBClient


class TimeUserBaseDBClient(UserBaseDBClient[BaseModel]):
    def __init__(self, model: Type[BaseModel], user_id: uuid.UUID):
        super().__init__(model, user_id)

    def get_latest(self) -> BaseModel:
        with self.session as session:
            statement = (
                select(self.model)
                .where(self.model.user_id == self.user_id)
                .order_by(self.model.timestamp.desc())
                .limit(1)
            )
            result = session.exec(statement)
            return result.one_or_none()
