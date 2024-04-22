from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from lifehub.models.util.module_provider import ModuleProvider

if TYPE_CHECKING:
    from lifehub.models.util import Module


class ProviderType(str, Enum):
    basic = "basic"
    token = "token"
    oauth = "oauth"


class Provider(SQLModel, table=True):
    id: int = Field(primary_key=True, sa_column_args={"autoincrement": True})
    name: str = Field(max_length=32, unique=True, nullable=False)
    type: ProviderType = Field(nullable=False)

    modules: list["Module"] = Relationship(
        back_populates="providers", link_model=ModuleProvider
    )
