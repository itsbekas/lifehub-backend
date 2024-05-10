from typing import Type

from sqlalchemy import Session, select

from lifehub.core.common.repository import BaseModelType
from lifehub.core.common.repository.base import BaseRepository
from lifehub.core.user.schema import User


class UserBaseRepository(BaseRepository[BaseModelType]):
    def __init__(self, model: Type[BaseModelType], user: User, session: Session):
        super().__init__(model, session)
        self.user: User = user

    def add(self, obj: BaseModelType):
        if obj.user_id == self.user.id:
            super().add(obj)
        else:
            raise ValueError("User ID does not match")

    def get_one_or_none(self) -> BaseModelType:
        statement = select(self.model).where(self.model.user_id == self.user.id)
        result = self.session.exec(statement)
        return result.one_or_none()

    def get_all(self) -> list[BaseModelType]:
        statement = select(self.model).where(self.model.user_id == self.user.id)
        result = self.session.exec(statement)
        return result.all()

    def update(self, obj: BaseModelType) -> BaseModelType:
        if obj.user_id == self.user.id:
            return super().update(obj)
        raise ValueError("User ID does not match")

    def delete(self, obj: BaseModelType) -> None:
        if obj.user_id == self.user.id:
            return super().delete(obj)
        raise ValueError("User ID does not match")
