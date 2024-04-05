import datetime
from decimal import Decimal

from sqlmodel import Field, SQLModel


class Networth(SQLModel, table=True):
    timestamp: datetime.datetime = Field(
        default_factory=datetime.datetime.now, primary_key=True
    )
    bank_cash: Decimal = Field(default=0, decimal_places=2, max_digits=10)
    uninvested_cash: Decimal = Field(default=0, decimal_places=2, max_digits=10)
    invested: Decimal = Field(default=0, decimal_places=2, max_digits=10)
    returns: Decimal = Field(default=0, decimal_places=2, max_digits=10)
    total: Decimal = Field(default=0, decimal_places=2, max_digits=10)
