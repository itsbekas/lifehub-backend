from sqlalchemy import Session

from lifehub.core.common.repository.fetch_base import FetchBaseRepository
from lifehub.core.user.schema import User
from lifehub.providers.qbittorrent.schema import QBittorrentStats


class QBittorrentStatsRepository(FetchBaseRepository[QBittorrentStats]):
    def __init__(self, user: User, session: Session):
        super().__init__(QBittorrentStats, user, session)
