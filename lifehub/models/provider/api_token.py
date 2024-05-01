import datetime as dt
import uuid

from sqlmodel import Field, Relationship, SQLModel

from lifehub.models.user.user import User


class APIToken(SQLModel, table=True):
    user_id: uuid.UUID = Field(primary_key=True, foreign_key="user.id")
    provider_id: int = Field(primary_key=True, foreign_key="provider.id")
    token: str = Field(max_length=128, nullable=False)
    refresh_token: str = Field(max_length=128, nullable=True)
    created_at: dt.datetime = Field(default_factory=dt.datetime.now)
    expires_at: dt.datetime = Field(default=dt.datetime.max)

    user: User = Relationship(
        back_populates="api_tokens", sa_relationship_kwargs={"cascade": "all, delete"}
    )
