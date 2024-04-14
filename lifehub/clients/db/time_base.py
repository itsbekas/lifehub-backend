from sqlmodel import select

from .base import BaseDBClient, BaseModel


class TimeBaseDBClient(BaseDBClient[BaseModel]):
    def get_latest(self) -> BaseModel:
        with self.session as session:
            statement = select(self.model).order_by(self.model.date.desc()).limit(1)
            result = session.exec(statement)
            return result.one_or_none()
