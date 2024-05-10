from sqlalchemy import Session

from lifehub.clients.db.base import TimeUserBaseDBClient
from lifehub.core.user.schema import User
from lifehub.providers.qbittorrent.schema import QBittorrentStats


class QBittorrentStatsDBClient(TimeUserBaseDBClient[QBittorrentStats]):
    def __init__(self, user: User, session: Session):
        super().__init__(QBittorrentStats, user, session)
