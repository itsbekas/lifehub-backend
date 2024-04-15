import uuid

from lifehub.clients.db.time_user_base import TimeUserBaseDBClient
from lifehub.models.server import QBittorrentStats


class QBittorrentStatsDBClient(TimeUserBaseDBClient[QBittorrentStats]):
    def __init__(self, user_id: uuid.UUID):
        super().__init__(QBittorrentStats, user_id)
