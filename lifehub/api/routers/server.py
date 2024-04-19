from typing import Annotated

from fastapi import APIRouter, Depends

from lifehub.api.exceptions.user import NoDataForUserException
from lifehub.api.routers.dependencies import get_user_id
from lifehub.clients.db.server import QBittorrentStatsDBClient
from lifehub.models.server import QBittorrentStats

router = APIRouter(
    prefix="/server",
    tags=["server"],
)


@router.get("/qbit-stats", response_model=QBittorrentStats)
async def stats(user_id: Annotated[str, Depends(get_user_id)]):
    db_client = QBittorrentStatsDBClient(user_id)
    stats = db_client.get_latest()

    if stats is None:
        raise NoDataForUserException()

    return stats
