import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from lifehub.models.user.user import User


class UserToken(SQLModel, table=True):
    user_id: uuid.UUID = Field(primary_key=True, foreign_key="user.id")
    access_token: str = Field(max_length=256, nullable=False)
    token_type: str = Field(max_length=16, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)
    expires_at: datetime = Field()

    user: "User" = Relationship(back_populates="token")
