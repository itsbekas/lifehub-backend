from fastapi import APIRouter, HTTPException
from sqlalchemy import exc as sa_exc
from sqlmodel import SQLModel

from lifehub.core.common.api.dependencies import ModuleDep, SessionDep, UserDep
from lifehub.models.provider.provider import Provider

router = APIRouter()


class ModuleWithProviders(SQLModel):
    id: int
    name: str
    providers: list[Provider]


@router.get("", response_model=list[ModuleWithProviders])
async def get_user_modules(user: UserDep):
    return user.modules


@router.post("/{module_id}")
async def add_user_module(
    user: UserDep,
    session: SessionDep,
    module: ModuleDep,
):
    user = session.merge(user)
    module = session.merge(module)

    missed_providers = []

    for provider in module.providers:
        if provider not in user.providers:
            missed_providers.append(provider.name)

    if missed_providers:
        raise HTTPException(
            403, f"User is missing providers: {', '.join(missed_providers)}"
        )

    user.modules.append(module)
    session.add(user)

    try:
        session.commit()
    except sa_exc.IntegrityError as e:
        session.rollback()
        match e.orig.errno:
            case 1062:
                raise HTTPException(409, f"User already has module {module.name}")
            case _:
                raise e


@router.delete("/{module_id}")
async def remove_user_module(
    user: UserDep,
    session: SessionDep,
    module: ModuleDep,
):
    user = session.merge(user)
    module = session.merge(module)

    if module not in user.modules:
        raise HTTPException(404, f"User does not have module {module.name}")

    user.modules.remove(module)
    session.add(user)
    session.commit()
