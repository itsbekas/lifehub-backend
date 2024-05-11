from fastapi import APIRouter, Depends

from lifehub.core.user.api.dependencies import user_is_authenticated

router = APIRouter(
    dependencies=[Depends(user_is_authenticated)],
)


# @router.get("", response_model=list[ModuleWithProvidersResponse])
# async def get_user_modules(user: UserDep):
#     return user.modules


# @router.post("/{module_id}")
# async def add_user_module(
#     user: UserDep,
#     session: SessionDep,
#     module: ModuleDep,
# ):
#     user = session.merge(user)
#     module = session.merge(module)

#     missed_providers = []

#     for provider in module.providers:
#         if provider not in user.providers:
#             missed_providers.append(provider.name)

#     if missed_providers:
#         raise HTTPException(
#             403, f"User is missing providers: {', '.join(missed_providers)}"
#         )

#     user.modules.append(module)
#     session.add(user)

#     try:
#         session.commit()
#     except sa_exc.IntegrityError as e:
#         session.rollback()
#         match e.orig.errno:
#             case 1062:
#                 raise HTTPException(409, f"User already has module {module.name}")
#             case _:
#                 raise e


# @router.delete("/{module_id}")
# async def remove_user_module(
#     user: UserDep,
#     session: SessionDep,
#     module: ModuleDep,
# ):
#     user = session.merge(user)
#     module = session.merge(module)

#     if module not in user.modules:
#         raise HTTPException(404, f"User does not have module {module.name}")

#     user.modules.remove(module)
#     session.add(user)
#     session.commit()
