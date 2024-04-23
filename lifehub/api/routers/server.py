from typing import Annotated

from fastapi import APIRouter, Depends

from lifehub.api.exceptions.user import NoDataForUserException
from lifehub.api.routers.dependencies import get_user
from lifehub.clients.db.server import QBittorrentStatsDBClient
from lifehub.models.server import QBittorrentStats
from lifehub.models.user import User

router = APIRouter(
    prefix="/server",
    tags=["server"],
)


@router.get("/qbit-stats", response_model=QBittorrentStats)
async def stats(user: Annotated[User, Depends(get_user)]):
    db_client = QBittorrentStatsDBClient(user.id)
    stats = db_client.get_latest()

    if stats is None:
        raise NoDataForUserException()

    return stats
