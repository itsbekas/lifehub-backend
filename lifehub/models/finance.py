import datetime as dt
import uuid
from decimal import Decimal

from sqlalchemy import DECIMAL, BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from lifehub.models.base import BaseModel


class T212Transaction(BaseModel):
    __tablename__ = "t212_transaction"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    timestamp: Mapped[dt.datetime] = mapped_column(index=True)


class Networth(BaseModel):
    __tablename__ = "networth"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), primary_key=True)
    timestamp: Mapped[dt.datetime] = mapped_column(primary_key=True)
    bank: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    uninvested: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    invested: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    returns: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    total: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))


class YNABBalance(BaseModel):
    __tablename__ = "ynab_balance"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), primary_key=True)
    timestamp: Mapped[dt.datetime] = mapped_column(
        default=dt.datetime.now, primary_key=True
    )
    balance: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))


class T212Balance(BaseModel):
    __tablename__ = "t212_balance"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), primary_key=True)
    timestamp: Mapped[dt.datetime] = mapped_column(
        default=dt.datetime.now, primary_key=True
    )
    free: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    invested: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    result: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))


class T212Order(BaseModel):
    __tablename__ = "t212_order"

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    ticker: Mapped[str] = mapped_column(String(10))
    quantity: Mapped[Decimal] = mapped_column(DECIMAL(15, 7))
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    timestamp: Mapped[dt.datetime] = mapped_column(index=True)
