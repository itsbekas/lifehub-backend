import datetime as dt
import uuid

from sqlmodel import Field, SQLModel


class APIToken(SQLModel, table=True):
    provider: str = Field(max_length=32, default=None, primary_key=True)
    token: str = Field(max_length=128)
    user_id: uuid.UUID = Field(primary_key=True)
    created_at: dt.datetime = Field(default_factory=dt.datetime.now)
    expires_at: dt.datetime = Field()
