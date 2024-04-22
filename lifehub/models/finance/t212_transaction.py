import datetime
import uuid
from decimal import Decimal

from sqlalchemy import BigInteger, Column
from sqlmodel import Field, SQLModel


class T212Transaction(SQLModel, table=True):
    id: int = Field(sa_column=Column(BigInteger(), primary_key=True))
    user_id: uuid.UUID = Field(foreign_key="user.id")
    amount: Decimal = Field(decimal_places=2, max_digits=10)
    timestamp: datetime.datetime = Field(index=True)
