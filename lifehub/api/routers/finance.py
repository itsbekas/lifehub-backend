from typing import Annotated

from fastapi import APIRouter, Depends

from lifehub.api.exceptions.user import NoDataForUserException
from lifehub.api.routers.dependencies import get_user
from lifehub.clients.db.finance import NetworthDBClient
from lifehub.models.finance import Networth
from lifehub.models.user import User

router = APIRouter(
    prefix="/finance",
    tags=["finance"],
)


@router.get("/networth", response_model=Networth)
async def networth(
    user: Annotated[User, Depends(get_user)],
):
    db_client = NetworthDBClient(user.id)
    networth = db_client.get_latest()

    if networth is None:
        raise NoDataForUserException()

    return networth
