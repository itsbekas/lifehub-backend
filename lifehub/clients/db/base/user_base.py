from typing import Type

from sqlmodel import select

from lifehub.clients.db.base.base import BaseDBClient, BaseModel
from lifehub.models.user import User


class UserBaseDBClient(BaseDBClient[BaseModel]):
    def __init__(self, model: Type[BaseModel], user: User):
        super().__init__(model)
        self.user: User = user

    def add(self, obj: BaseModel) -> BaseModel:
        if obj.user_id == self.user.id:
            return super().add(obj)
        raise ValueError("User ID does not match")

    def get_one_or_none(self) -> BaseModel:
        with self.session as session:
            statement = select(self.model).where(self.model.user_id == self.user.id)
            result = session.exec(statement)
            return result.one_or_none()

    def get_all(self) -> list[BaseModel]:
        with self.session as session:
            statement = select(self.model).where(self.model.user_id == self.user.id)
            result = session.exec(statement)
            return result.all()

    def update(self, obj: BaseModel) -> BaseModel:
        if obj.user_id == self.user.id:
            return super().update(obj)
        raise ValueError("User ID does not match")

    def delete(self, obj: BaseModel) -> None:
        if obj.user_id == self.user.id:
            return super().delete(obj)
        raise ValueError("User ID does not match")
