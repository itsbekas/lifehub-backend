from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from lifehub.api.routers.dependencies import get_user_id, get_session
from lifehub.clients.db.networth import NetworthDBClient
from lifehub.models.finance import Networth
import uuid
from lifehub.api.lib.exceptions import NoDataForUserException

router = APIRouter(
    prefix="/finance",
    tags=["finance"],
)


@router.get("/networth", response_model=Networth)
async def networth(
    user_id: Annotated[uuid.UUID, Depends(get_user_id)],
):
    db_client = NetworthDBClient(user_id)
    networth = db_client.get_latest()

    if networth is None:
        raise NoDataForUserException()

    return networth
