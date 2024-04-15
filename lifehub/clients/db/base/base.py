from typing import Generic, List, Type, TypeVar

from sqlmodel import Session, SQLModel, select

from lifehub.clients.db.service import DatabaseService

BaseModel = TypeVar("BaseModel", bound=SQLModel)


class BaseDBClient(Generic[BaseModel]):
    def __init__(self, model: Type[BaseModel]):
        self.model: Type[BaseModel] = model
        self.session: Session = DatabaseService().get_session()

    def add(self, obj: BaseModel) -> BaseModel:
        with self.session as session:
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj

    def get_all(self) -> List[BaseModel]:
        with self.session as session:
            statement = select(self.model)
            result = session.exec(statement)
            return result.all()

    def update(self, obj: BaseModel) -> BaseModel:
        with self.session as session:
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj

    def delete(self, obj: BaseModel) -> None:
        with self.session as session:
            session.delete(obj)
            session.commit()
