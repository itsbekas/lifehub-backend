from fastapi import APIRouter

from lifehub.clients.db.server import QBittorrentStatsDBClient
from lifehub.core.api_dependencies import SessionDep, UserDep
from lifehub.core.api_exceptions import NoUserDataForModuleException
from lifehub.modules.server.schema import QBittorrentStats

router = APIRouter()


@router.get("/qbit-stats", response_model=QBittorrentStats)
async def stats(user: UserDep, session: SessionDep) -> QBittorrentStats:
    db_client = QBittorrentStatsDBClient(user.id)
    stats = db_client.get_latest()

    if stats is None:
        raise NoUserDataForModuleException(user.username, "qbit-stats")

    return stats
