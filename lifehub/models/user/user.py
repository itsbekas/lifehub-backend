import datetime as dt
import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from lifehub.models.user.user_token import UserToken

if TYPE_CHECKING:
    from lifehub.models.provider import APIToken, Provider
    from lifehub.models.util import Module


class UserProviderLink(SQLModel, table=True):
    user_id: uuid.UUID = Field(foreign_key="user.id", primary_key=True)
    provider_id: int = Field(foreign_key="provider.id", primary_key=True)


class UserModuleLink(SQLModel, table=True):
    user_id: uuid.UUID = Field(primary_key=True, foreign_key="user.id")
    module_id: int = Field(primary_key=True, foreign_key="module.id")


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(max_length=32, unique=True, nullable=False)
    password: str = Field(max_length=128, nullable=False)
    name: str = Field(max_length=64, nullable=False)
    created_at: dt.datetime = Field(default_factory=dt.datetime.now)

    modules: list["Module"] = Relationship(
        back_populates="users", link_model=UserModuleLink
    )
    providers: list["Provider"] = Relationship(
        back_populates="users", link_model=UserProviderLink
    )
    api_tokens: list["APIToken"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    token: UserToken = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"}
    )
