import datetime as dt
import uuid
from decimal import Decimal

from sqlalchemy import BigInteger, Column
from sqlmodel import Field, SQLModel


class QBittorrentStats(SQLModel, table=True):
    user_id: uuid.UUID = Field(foreign_key="user.id")
    timestamp: dt.datetime = Field(
        default_factory=dt.datetime.now, primary_key=True, index=True
    )
    alltime_dl: int = Field(sa_column=Column(BigInteger()))
    alltime_ul: int = Field(sa_column=Column(BigInteger()))
    alltime_ratio: Decimal = Field(decimal_places=2, max_digits=5)
