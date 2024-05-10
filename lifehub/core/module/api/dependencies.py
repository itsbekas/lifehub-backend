from typing import Annotated

from fastapi import Depends, HTTPException

from lifehub.core.module.schema import Module
from lifehub.core.module.service.module import ModuleService

ModuleServiceDep = Annotated[ModuleService, Depends(ModuleService)]


def get_module(
    module_id: int,
    module_service: ModuleServiceDep,
) -> Module:
    try:
        module = module_service.get_module_by_id(module_id)
    except Exception:
        raise HTTPException(404, "Module not found")

    return module


ModuleDep = Annotated[Module, Depends(get_module)]
