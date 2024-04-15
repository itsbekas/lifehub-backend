from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from lifehub.api.routers.dependencies import get_session, get_user_id
from lifehub.models.server import QBittorrentStats

router = APIRouter(
    prefix="/server",
    tags=["server"],
)


@router.get("/qbit-stats", response_model=QBittorrentStats)
async def stats(
    user_id: Annotated[str, Depends(get_user_id)],
    session: Session = Depends(get_session),
):
    with session as s:
        query = select(QBittorrentStats).order_by(QBittorrentStats.timestamp.desc())
        stats = s.exec(query).first()

    return stats
