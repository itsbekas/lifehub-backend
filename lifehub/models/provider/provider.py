from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lifehub.models.user import User
    from lifehub.models.util import Module

from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lifehub.models.base import BaseModel


class ProviderType(str, Enum):
    basic = "basic"
    token = "token"
    oauth = "oauth"


class Provider(BaseModel):
    __tablename__ = "provider"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)
    type: Mapped[ProviderType] = mapped_column(String(16))

    modules: Mapped[List["Module"]] = relationship(back_populates="providers")

    users: Mapped[List["User"]] = relationship(back_populates="providers")
