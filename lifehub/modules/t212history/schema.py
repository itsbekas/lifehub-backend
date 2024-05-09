import datetime as dt
import uuid
from decimal import Decimal

from sqlalchemy import DECIMAL, BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from lifehub.core.base_model import BaseModel


class T212Transaction(BaseModel):
    __tablename__ = "t212_transaction"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    timestamp: Mapped[dt.datetime] = mapped_column(index=True)


class T212Order(BaseModel):
    __tablename__ = "t212_order"

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    ticker: Mapped[str] = mapped_column(String(10))
    quantity: Mapped[Decimal] = mapped_column(DECIMAL(15, 7))
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    timestamp: Mapped[dt.datetime] = mapped_column(index=True)
