import datetime
from decimal import Decimal

from sqlmodel import Field, SQLModel


class Networth(SQLModel, table=True):
    timestamp: datetime.datetime = Field(
        default_factory=datetime.datetime.now, primary_key=True, index=True
    )
    bank_cash: Decimal = Field(decimal_places=2, max_digits=10)
    uninvested_cash: Decimal = Field(decimal_places=2, max_digits=10)
    invested: Decimal = Field(decimal_places=2, max_digits=10)
    returns: Decimal = Field(decimal_places=2, max_digits=10)
    total: Decimal = Field(decimal_places=2, max_digits=10)
