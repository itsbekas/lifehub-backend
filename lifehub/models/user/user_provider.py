import uuid

from sqlmodel import Field, SQLModel


class UserProvider(SQLModel, table=True):
    user_id: uuid.UUID = Field(foreign_key="user.id", primary_key=True)
    provider_id: int = Field(foreign_key="provider.id", primary_key=True)
