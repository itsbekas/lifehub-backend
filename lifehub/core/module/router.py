from fastapi import APIRouter

from lifehub.core.common.api.dependencies import SessionDep
from lifehub.core.module.repository.module import ModuleRepository
from lifehub.core.module.schema import Module

router = APIRouter()


@router.get("", response_model=list[Module])
async def get_modules(
    session: SessionDep,
):
    return ModuleRepository(session).get_all()
