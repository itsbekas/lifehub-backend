import uuid
from typing import Type

from sqlmodel import select

from .base import BaseModel
from .user_base import UserBaseDBClient


class TimeUserBaseDBClient(UserBaseDBClient[BaseModel]):
    def __init__(self, model: Type[BaseModel], user_id: uuid.UUID):
        super().__init__(model, user_id)

    def get_latest(self) -> BaseModel:
        with self.session() as session:
            statement = (
                select(self.model)
                .where(self.model.user_id == self.user_id)
                .order_by(self.model.date.desc())
                .limit(1)
            )
            result = session.exec(statement)
            return result.one()
