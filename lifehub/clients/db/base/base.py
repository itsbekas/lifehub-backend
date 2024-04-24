from typing import Generic, List, Type, TypeVar

from sqlmodel import Session, SQLModel, select

BaseModel = TypeVar("BaseModel", bound=SQLModel)


class BaseDBClient(Generic[BaseModel]):
    def __init__(self, model: Type[BaseModel], session: Session):
        self.model: Type[BaseModel] = model
        self.session = session

    def add(self, obj: BaseModel) -> None:
        self.session.add(obj)

    def get_all(self) -> List[BaseModel]:
        statement = select(self.model)
        result = self.session.exec(statement)
        return result.all()

    def update(self, obj: BaseModel) -> None:
        self.session.add(obj)

    def delete(self, obj: BaseModel) -> None:
        self.session.delete(obj)

    def commit(self):
        self.session.commit()

    def refresh(self, obj: BaseModel):
        self.session.refresh(obj)

    def rollback(self):
        self.session.rollback()
