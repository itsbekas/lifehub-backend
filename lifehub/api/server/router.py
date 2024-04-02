from typing import Annotated

from fastapi import APIRouter, Depends

from lifehub.api.auth.lib import oauth2_scheme

from .lib import get_qbit_server_state
from .schemas import AllTimeStats

router = APIRouter(
    prefix="/server",
    tags=["server"],
)


@router.get("/qbit-stats", response_model=AllTimeStats)
async def stats(token: Annotated[str, Depends(oauth2_scheme)]):
    return AllTimeStats.from_obj(get_qbit_server_state())
