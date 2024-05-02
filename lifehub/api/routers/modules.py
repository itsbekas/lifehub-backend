from fastapi import APIRouter

from lifehub.api.routers.dependencies import SessionDep
from lifehub.clients.db.util.module import ModuleDBClient
from lifehub.models.util.module import Module

router = APIRouter()


@router.get("", response_model=list[Module])
async def get_modules(
    session: SessionDep,
):
    return ModuleDBClient(session).get_all()
