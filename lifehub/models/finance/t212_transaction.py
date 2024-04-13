import datetime
import uuid
from decimal import Decimal

from sqlmodel import Field, SQLModel


class T212Transaction(SQLModel, table=True):
    user_id: uuid.UUID = Field(foreign_key="user.id")
    type: str = Field(max_length=10)  # TODO: get the correct length (maybe Enum?)
    amount: Decimal = Field(decimal_places=2, max_digits=10)
    id: str = Field(max_length=128, primary_key=True)  # TODO: get the correct length
    timestamp: datetime.datetime = Field(index=True)
