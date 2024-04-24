import datetime
import uuid
from decimal import Decimal

from sqlmodel import Field, SQLModel


class T212Transaction(SQLModel, table=True):
    id: str = Field(primary_key=True, max_length=64)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    amount: Decimal = Field(decimal_places=2, max_digits=10)
    timestamp: datetime.datetime = Field(index=True)
