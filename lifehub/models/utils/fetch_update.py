from datetime import datetime

from sqlmodel import Field, SQLModel


class FetchUpdate(SQLModel, table=True):
    id: str = Field(max_length=32, primary_key=True)
    last_update: datetime = Field(default=datetime.min)
