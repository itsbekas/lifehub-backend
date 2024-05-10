from fastapi import APIRouter

from lifehub.core.module.repository.module import ModuleRepository
from lifehub.core.module.schema import Module
from lifehub.core.user.api.dependencies import SessionDep

router = APIRouter()


@router.get("", response_model=list[Module])
async def get_modules(
    session: SessionDep,
):
    return ModuleRepository(session).get_all()
