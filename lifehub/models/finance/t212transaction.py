import datetime
from decimal import Decimal

from sqlmodel import Field, SQLModel


class T212Transaction(SQLModel, table=True):
    ticker: str = Field(max_length=10, primary_key=True)
    quantity: Decimal = Field(decimal_places=7, max_digits=10)
    price: Decimal = Field(decimal_places=2, max_digits=10)
    timestamp: datetime.datetime = Field(
        default_factory=datetime.datetime.now, primary_key=True
    )
