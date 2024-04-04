import datetime
from decimal import Decimal

from sqlmodel import Field, SQLModel


class Networth(SQLModel, table=True):
    timestamp: datetime.datetime = Field(
        default_factory=datetime.datetime.now, primary_key=True
    )
    cash: Decimal = Field(default=0, decimal_places=2, max_digits=10)
    investments: Decimal = Field(default=0, decimal_places=2, max_digits=10)
