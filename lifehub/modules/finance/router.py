from fastapi import APIRouter

from lifehub.clients.db.finance import NetworthDBClient
from lifehub.core.api_dependencies import SessionDep, UserDep
from lifehub.core.api_exceptions import NoUserDataForModuleException
from lifehub.providers.ynab.schema import Networth

router = APIRouter()


@router.get("/networth", response_model=Networth)
async def networth(
    user: UserDep,
    session: SessionDep,
):
    db_client = NetworthDBClient(user, session)
    networth = db_client.get_latest()

    if networth is None:
        raise NoUserDataForModuleException(user.username, "networth")

    return networth
