import datetime as dt
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lifehub.models.base import BaseModel

if TYPE_CHECKING:
    from lifehub.models.module import Module
    from lifehub.models.provider import Provider, ProviderToken


user_provider = Table(
    "user_provider",
    BaseModel.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("provider_id", ForeignKey("provider.id"), primary_key=True),
)


user_module = Table(
    "user_module",
    BaseModel.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("module_id", ForeignKey("module.id"), primary_key=True),
)


class User(BaseModel):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[dt.datetime] = mapped_column(default=dt.datetime.now)

    modules: Mapped[list["Module"]] = relationship(
        secondary=user_module, back_populates="users"
    )
    providers: Mapped[list["Provider"]] = relationship(
        secondary=user_provider, back_populates="users"
    )
    api_tokens: Mapped[list["ProviderToken"]] = relationship(back_populates="user")
