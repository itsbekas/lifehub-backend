from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from lifehub.models.user import UserModule
from lifehub.models.util.module_provider import ModuleProvider

if TYPE_CHECKING:
    from lifehub.models.provider.provider import Provider
    from lifehub.models.user import User


class Module(SQLModel, table=True):
    id: int = Field(primary_key=True, sa_column_kwargs={"autoincrement": True})
    name: str = Field(max_length=32, unique=True, nullable=False)

    providers: list["Provider"] = Relationship(
        back_populates="modules", link_model=ModuleProvider
    )

    users: list["User"] = Relationship(back_populates="modules", link_model=UserModule)
