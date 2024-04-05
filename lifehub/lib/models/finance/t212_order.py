import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, Column
from sqlmodel import Field, SQLModel


class T212Order(SQLModel, table=True):
    type: str = Field(max_length=10)  # TODO: get the correct length (maybe Enum?)
    id: int = Field(sa_column=Column(BigInteger(), primary_key=True))
    ticker: str = Field(max_length=10)  # TODO: get the correct length
    quantity: Decimal = Field(decimal_places=7, max_digits=15)
    price: Decimal = Field(decimal_places=2, max_digits=10)
    timestamp: datetime.datetime = Field()
