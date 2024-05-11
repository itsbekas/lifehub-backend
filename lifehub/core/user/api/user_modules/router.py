from fastapi import APIRouter, Depends

from lifehub.core.module.api.dependencies import ModuleDep
from lifehub.core.module.models import ModuleResponse
from lifehub.core.user.api.dependencies import (
    UserDep,
    UserServiceDep,
    user_is_authenticated,
)

router = APIRouter(
    dependencies=[Depends(user_is_authenticated)],
)


@router.get("", response_model=list[ModuleResponse])
async def get_user_modules(user: UserDep, user_service: UserServiceDep):
    return user_service.get_user_modules(user)


@router.post("/{module_id}")
async def add_user_module(
    user: UserDep,
    module: ModuleDep,
    user_service: UserServiceDep,
):
    try:
        user_service.add_module_to_user(user, module)
    except Exception as e:
        # TODO: API exception (#28)
        raise e


@router.delete("/{module_id}")
async def remove_user_module(
    user: UserDep,
    module: ModuleDep,
    user_service: UserServiceDep,
):
    try:
        user_service.remove_module_from_user(user, module)
    except Exception as e:
        # TODO: API exception (#28)
        raise e
