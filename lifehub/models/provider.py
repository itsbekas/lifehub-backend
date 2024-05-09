import datetime as dt
import uuid
from enum import Enum
from os import getenv
from typing import TYPE_CHECKING, List

from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lifehub.models.base import BaseModel
from lifehub.models.module import module_provider
from lifehub.models.user import user_provider

if TYPE_CHECKING:
    from lifehub.models.module import Module
    from lifehub.models.provider import Provider
    from lifehub.models.user import User


def oauth_redirect_uri() -> str:
    return getenv("REDIRECT_URI_BASE") + "/account/oauth_token"


class ProviderType(str, Enum):
    basic = "basic"
    token = "token"
    oauth = "oauth"


class Provider(BaseModel):
    __tablename__ = "provider"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)
    type: Mapped[ProviderType] = mapped_column(String(16))

    modules: Mapped[List["Module"]] = relationship(
        secondary=module_provider, back_populates="providers"
    )
    users: Mapped[List["User"]] = relationship(
        secondary=user_provider, back_populates="providers"
    )


class ProviderToken(BaseModel):
    __tablename__ = "provider_token"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), primary_key=True
    )
    provider_id: Mapped[int] = mapped_column(
        ForeignKey("provider.id"), primary_key=True
    )
    custom_url: Mapped[str] = mapped_column(String(64), nullable=True)
    token: Mapped[str] = mapped_column(String(128), nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(128), nullable=True)
    created_at: Mapped[dt.datetime] = mapped_column(default=dt.datetime.now)
    expires_at: Mapped[dt.datetime] = mapped_column(default=dt.datetime.max)

    user: Mapped["User"] = relationship(back_populates="api_tokens")
