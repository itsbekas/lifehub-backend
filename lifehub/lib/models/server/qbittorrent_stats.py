import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, Column
from sqlmodel import Field, SQLModel


class QBittorrentStats(SQLModel, table=True):
    timestamp: datetime.datetime = Field(
        default_factory=datetime.datetime.now, primary_key=True, index=True
    )
    alltime_dl: int = Field(sa_column=Column(BigInteger()))
    alltime_ul: int = Field(sa_column=Column(BigInteger()))
    alltime_ratio: Decimal = Field(decimal_places=2, max_digits=5)
