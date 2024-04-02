from typing import Annotated

from fastapi import APIRouter, Depends

from lifehub.api.auth.lib import oauth2_scheme
from lifehub.lib.server.qbittorrent import get_server_state

from .models import AllTimeStats

router = APIRouter(
    prefix="/server",
    tags=["server"],
)


@router.get("/qbit-stats", response_model=AllTimeStats)
async def stats(token: Annotated[str, Depends(oauth2_scheme)]):
    return AllTimeStats.from_obj(get_server_state())
