from sqlmodel import Session

from lifehub.clients.db.base import TimeUserBaseDBClient
from lifehub.models.server import QBittorrentStats
from lifehub.models.user import User


class QBittorrentStatsDBClient(TimeUserBaseDBClient[QBittorrentStats]):
    def __init__(self, user: User, session: Session):
        super().__init__(QBittorrentStats, user, session)
