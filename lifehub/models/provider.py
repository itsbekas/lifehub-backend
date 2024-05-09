from __future__ import annotations

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

    config: Mapped[ProviderConfig] = relationship(
        back_populates="provider", uselist=False
    )

    modules: Mapped[List[Module]] = relationship(
        secondary=module_provider, back_populates="providers"
    )
    users: Mapped[List[User]] = relationship(
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

    user: Mapped[User] = relationship(back_populates="api_tokens")


class ProviderConfig(BaseModel):
    __tablename__ = "provider_config"

    provider_id: Mapped[int] = mapped_column(
        ForeignKey("provider.id"), primary_key=True
    )
    auth_type: Mapped[str] = mapped_column(String(64), nullable=False)
    allow_custom_url: Mapped[bool] = mapped_column(default=False)

    provider: Mapped[Provider] = relationship(
        back_populates="config", single_parent=True
    )

    __mapper_args__ = {
        "polymorphic_identity": "provider_config",
        "polymorphic_on": auth_type,
    }


class OAuthProviderConfig(ProviderConfig):
    __tablename__ = "oauth_provider_config"

    provider_id: Mapped[int] = mapped_column(
        ForeignKey("provider_config.provider_id"), primary_key=True
    )
    auth_url: Mapped[str] = mapped_column(String(64), nullable=False)
    token_url: Mapped[str] = mapped_column(String(64), nullable=False)
    client_id: Mapped[str] = mapped_column(String(64), nullable=False)
    client_secret: Mapped[str] = mapped_column(String(64), nullable=False)
    scope: Mapped[str] = mapped_column(String(64), nullable=False)

    def build_auth_url(self) -> str:
        return f"{self.auth_url}?client_id={self.client_id}&redirect_uri={oauth_redirect_uri()}&scope={self.scope}&response_type=code&state={self.provider_id}"

    def build_token_url(self, auth_code: str) -> str:
        return f"{self.token_url}?client_id={self.client_id}&redirect_uri={oauth_redirect_uri()}&scope={self.scope}&grant_type=authorization_code&client_secret={self.client_secret}&code={auth_code}"

    def build_refresh_token_url(self, refresh_token: str) -> str:
        return f"{self.token_url}?client_id={self.client_id}&redirect_uri={oauth_redirect_uri()}&scope={self.scope}&grant_type=refresh_token&client_secret={self.client_secret}&refresh_token={refresh_token}"

    __mapper_args__ = {"polymorphic_identity": "oauth_provider_config"}


class TokenProviderConfig(ProviderConfig):
    __tablename__ = "token_provider_config"

    provider_id: Mapped[int] = mapped_column(
        ForeignKey("provider_config.provider_id"), primary_key=True
    )

    __mapper_args__ = {"polymorphic_identity": "token_provider_config"}


class BasicProviderConfig(ProviderConfig):
    __tablename__ = "basic_provider_config"

    provider_id: Mapped[int] = mapped_column(
        ForeignKey("provider_config.provider_id"), primary_key=True
    )

    __mapper_args__ = {"polymorphic_identity": "basic_provider_config"}
