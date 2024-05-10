from sqlalchemy import Session

from lifehub.core.common.repository.time_user_base import TimeUserBaseRepository
from lifehub.core.user.schema import User
from lifehub.providers.qbittorrent.schema import QBittorrentStats


class QBittorrentStatsRepository(TimeUserBaseRepository[QBittorrentStats]):
    def __init__(self, user: User, session: Session):
        super().__init__(QBittorrentStats, user, session)
