from decimal import Decimal

from sqlalchemy import DECIMAL, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from lifehub.core.common.base_model import FetchBaseModel


class QBittorrentStats(FetchBaseModel):
    __tablename__ = "qbit_stats"

    alltime_dl: Mapped[int] = mapped_column(BigInteger())
    alltime_ul: Mapped[int] = mapped_column(BigInteger())
    alltime_ratio: Mapped[Decimal] = mapped_column(DECIMAL(5, 2))
