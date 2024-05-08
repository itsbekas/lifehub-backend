from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lifehub.models.base import BaseModel

if TYPE_CHECKING:
    from lifehub.models.provider.provider import Provider


class Module(BaseModel):
    __tablename__ = "modules"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)

    providers: Mapped[List["Provider"]] = relationship(back_populates="provider")

    users = relationship("User", secondary="user_module_link")
