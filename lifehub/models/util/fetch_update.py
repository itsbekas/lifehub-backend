from datetime import datetime

from sqlmodel import Field, SQLModel


class FetchUpdate(SQLModel, table=True):
    module_id: int = Field(foreign_key="module.id", primary_key=True)
    last_update: datetime = Field(default=datetime.min)
