from sqlalchemy import select

from lifehub.clients.db.base.base import BaseDBClient, BaseModel


class TimeBaseDBClient(BaseDBClient[BaseModel]):
    def get_latest(self) -> BaseModel:
        statement = select(self.model).order_by(self.model.date.desc()).limit(1)
        result = self.session.exec(statement)
        return result.one_or_none()
