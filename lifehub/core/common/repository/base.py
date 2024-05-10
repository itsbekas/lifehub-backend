from typing import Generic, List, Type

from sqlalchemy import select
from sqlalchemy.orm import Session

from lifehub.core.common.repository import BaseModelType


class BaseRepository(Generic[BaseModelType]):
    def __init__(self, model: Type[BaseModelType], session: Session):
        self.model: Type[BaseModelType] = model
        self.session = session

    def add(self, obj: BaseModelType) -> None:
        self.session.add(obj)

    def get_all(self) -> List[BaseModelType]:
        statement = select(self.model)
        result = self.session.execute(statement)
        return result.all()

    def update(self, obj: BaseModelType) -> None:
        self.session.add(obj)

    def delete(self, obj: BaseModelType) -> None:
        self.session.delete(obj)

    def commit(self):
        self.session.commit()

    def refresh(self, obj: BaseModelType):
        self.session.refresh(obj)

    def rollback(self):
        self.session.rollback()

    def close(self):
        self.session.close()
