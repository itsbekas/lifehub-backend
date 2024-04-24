from fastapi import APIRouter

from lifehub.api.exceptions.user import NoDataForUserException
from lifehub.api.routers.dependencies import SessionDep, UserDep
from lifehub.clients.db.server import QBittorrentStatsDBClient
from lifehub.models.server import QBittorrentStats

router = APIRouter(
    prefix="/server",
    tags=["server"],
)


@router.get("/qbit-stats", response_model=QBittorrentStats)
async def stats(user: UserDep, session: SessionDep) -> QBittorrentStats:
    db_client = QBittorrentStatsDBClient(user.id)
    stats = db_client.get_latest()

    if stats is None:
        raise NoDataForUserException()

    return stats
