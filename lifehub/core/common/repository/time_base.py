from sqlalchemy import select

from lifehub.core.common.repository import BaseModelType
from lifehub.core.common.repository.base import BaseRepository


class TimeBaseRepository(BaseRepository[BaseModelType]):
    def get_latest(self) -> BaseModelType | None:
        statement = select(self.model).order_by(self.model.date.desc()).limit(1)
        result = self.session.exec(statement)
        return result.one_or_none()
