import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from lifehub.api.exceptions.user import NoDataForUserException
from lifehub.api.routers.dependencies import get_user_id
from lifehub.clients.db.finance import NetworthDBClient
from lifehub.models.finance import Networth

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
