import uuid

from sqlmodel import Field, SQLModel


class UserModule(SQLModel, table=True):
    user_id: uuid.UUID = Field(primary_key=True, foreign_key="user.id")
    module_id: int = Field(primary_key=True, foreign_key="module.id")
