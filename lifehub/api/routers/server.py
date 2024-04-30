from fastapi import APIRouter

from lifehub.api.exceptions import NoUserDataForModuleException
from lifehub.api.routers.dependencies import SessionDep, UserDep
from lifehub.clients.db.server import QBittorrentStatsDBClient
from lifehub.models.server import QBittorrentStats

router = APIRouter()


@router.get("/qbit-stats", response_model=QBittorrentStats)
async def stats(user: UserDep, session: SessionDep) -> QBittorrentStats:
    db_client = QBittorrentStatsDBClient(user.id)
    stats = db_client.get_latest()

    if stats is None:
        raise NoUserDataForModuleException(user.username, "qbit-stats")

    return stats
