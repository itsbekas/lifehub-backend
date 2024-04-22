import datetime
import uuid
from decimal import Decimal

from sqlmodel import Field, SQLModel


class Networth(SQLModel, table=True):
    user_id: uuid.UUID = Field(foreign_key="user.id")
    timestamp: datetime.datetime = Field(
        default_factory=datetime.datetime.now, primary_key=True
    )
    bank: Decimal = Field(decimal_places=2, max_digits=10)
    uninvested: Decimal = Field(decimal_places=2, max_digits=10)
    invested: Decimal = Field(decimal_places=2, max_digits=10)
    returns: Decimal = Field(decimal_places=2, max_digits=10)
    total: Decimal = Field(decimal_places=2, max_digits=10)
