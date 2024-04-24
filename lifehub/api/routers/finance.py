from fastapi import APIRouter

from lifehub.api.exceptions.user import NoDataForUserException
from lifehub.api.routers.dependencies import SessionDep, UserDep
from lifehub.clients.db.finance import NetworthDBClient
from lifehub.models.finance import Networth

router = APIRouter(
    prefix="/finance",
    tags=["finance"],
)


@router.get("/networth", response_model=Networth)
async def networth(
    user: UserDep,
    session: SessionDep,
):
    db_client = NetworthDBClient(user, session)
    networth = db_client.get_latest()

    if networth is None:
        raise NoDataForUserException()

    return networth
