from fastapi import APIRouter

from lifehub.clients.db.util.module import ModuleDBClient
from lifehub.core.common.api.dependencies import SessionDep
from lifehub.core.module.schema import Module

router = APIRouter()


@router.get("", response_model=list[Module])
async def get_modules(
    session: SessionDep,
):
    return ModuleDBClient(session).get_all()
