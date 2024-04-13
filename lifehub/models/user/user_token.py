import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel


class UserToken(SQLModel, table=True):
    user_id: uuid.UUID = Field(primary_key=True, nullable=False)
    token: str = Field(max_length=128, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)
