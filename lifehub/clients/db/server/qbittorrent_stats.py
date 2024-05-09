from sqlmodel import Session

from lifehub.clients.db.base import TimeUserBaseDBClient
from lifehub.models.user_old import User
from lifehub.modules.server.schema import QBittorrentStats


class QBittorrentStatsDBClient(TimeUserBaseDBClient[QBittorrentStats]):
    def __init__(self, user: User, session: Session):
        super().__init__(QBittorrentStats, user, session)
