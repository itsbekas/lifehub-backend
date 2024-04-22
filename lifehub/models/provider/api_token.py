import datetime as dt
import uuid

from sqlmodel import Field, SQLModel


class APIToken(SQLModel, table=True):
    user_id: uuid.UUID = Field(primary_key=True, foreign_key="user.id")
    provider_id: int = Field(primary_key=True, foreign_key="provider.id")
    token: str = Field(max_length=128, nullable=False)
    created_at: dt.datetime = Field(default_factory=dt.datetime.now)
    expires_at: dt.datetime = Field()
