import datetime as dt
import uuid

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(max_length=32, unique=True)
    password: str = Field(max_length=128)
    name: str = Field(max_length=32)
    created_at: dt.datetime = Field(default_factory=dt.datetime.now)
