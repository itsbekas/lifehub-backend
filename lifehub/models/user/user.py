import datetime as dt
import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from .user_module import UserModule

if TYPE_CHECKING:
    from lifehub.models.util import Module


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(max_length=32, unique=True, nullable=False)
    password: str = Field(max_length=128, nullable=False)
    name: str = Field(max_length=64, nullable=False)
    created_at: dt.datetime = Field(default_factory=dt.datetime.now)

    modules: list["Module"] = Relationship(
        back_populates="users", link_model=UserModule
    )
