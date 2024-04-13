import uuid
from typing import Type

from sqlmodel import select

from .base import BaseDBClient, BaseModel


class UserBaseDBClient(BaseDBClient[BaseModel]):
    def __init__(self, model: Type[BaseModel], user_id: uuid.UUID):
        super().__init__(model)
        self.user_id = user_id

    def add(self, obj: BaseModel) -> BaseModel:
        if obj.user_id == self.user_id:
            return super().add(obj)
        raise ValueError("User ID does not match")

    def get_all(self) -> list[BaseModel]:
        with self.session() as session:
            statement = select(self.model).where(self.model.user_id == self.user_id)
            result = session.exec(statement)
            return result.all()

    def update(self, obj: BaseModel) -> BaseModel:
        if obj.user_id == self.user_id:
            return super().update(obj)
        raise ValueError("User ID does not match")

    def delete(self, obj: BaseModel) -> None:
        if obj.user_id == self.user_id:
            return super().delete(obj)
        raise ValueError("User ID does not match")
