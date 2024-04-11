from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from lifehub.api.auth.lib import oauth2_scheme
from lifehub.lib.db import get_session
from lifehub.lib.models.server import AllTimeStats

server_router = APIRouter(
    prefix="/server",
    tags=["server"],
)


@server_router.get("/qbit-stats", response_model=AllTimeStats)
async def stats(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_session),
):
    with session as s:
        query = select(AllTimeStats).order_by(AllTimeStats.timestamp.desc())
        stats = s.exec(query).first()

    return stats
