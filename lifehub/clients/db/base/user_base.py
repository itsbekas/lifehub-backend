from typing import Type

from sqlmodel import Session, select

from lifehub.clients.db.base.base import BaseDBClient, BaseModel
from lifehub.models.user import User


class UserBaseDBClient(BaseDBClient[BaseModel]):
    def __init__(self, model: Type[BaseModel], user: User, session: Session):
        super().__init__(model, session)
        self.user: User = user

    def add(self, obj: BaseModel):
        if obj.user_id == self.user.id:
            super().add(obj)
        else:
            raise ValueError("User ID does not match")

    def get_one_or_none(self) -> BaseModel:
        statement = select(self.model).where(self.model.user_id == self.user.id)
        result = self.session.exec(statement)
        return result.one_or_none()

    def get_all(self) -> list[BaseModel]:
        statement = select(self.model).where(self.model.user_id == self.user.id)
        result = self.session.exec(statement)
        return result.all()

    def update(self, obj: BaseModel) -> BaseModel:
        if obj.user_id == self.user.id:
            return super().update(obj)
        raise ValueError("User ID does not match")

    def delete(self, obj: BaseModel) -> None:
        if obj.user_id == self.user.id:
            return super().delete(obj)
        raise ValueError("User ID does not match")
