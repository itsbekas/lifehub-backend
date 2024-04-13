from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from lifehub.api.routers.dependencies import oauth2_scheme
from lifehub.clients.db import get_session
from lifehub.models.server import QBittorrentStats

router = APIRouter(
    prefix="/server",
    tags=["server"],
)


@router.get("/qbit-stats", response_model=QBittorrentStats)
async def stats(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_session),
):
    with session as s:
        query = select(QBittorrentStats).order_by(QBittorrentStats.timestamp.desc())
        stats = s.exec(query).first()

    return stats
