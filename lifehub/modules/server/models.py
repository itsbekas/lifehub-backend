import datetime as dt
import uuid
from decimal import Decimal

from sqlalchemy import DECIMAL, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from lifehub.core.models.base import BaseModel


class QBittorrentStats(BaseModel):
    __tablename__ = "qbit_stats"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), primary_key=True)
    timestamp: Mapped[dt.datetime] = mapped_column(
        default=dt.datetime.now, primary_key=True
    )
    alltime_dl: Mapped[int] = mapped_column(BigInteger())
    alltime_ul: Mapped[int] = mapped_column(BigInteger())
    alltime_ratio: Mapped[Decimal] = mapped_column(DECIMAL(5, 2))
