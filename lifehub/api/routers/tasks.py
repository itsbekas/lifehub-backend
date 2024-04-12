# from lifehub.lib.models.tasks import Task

from fastapi import APIRouter

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


# @router.get("/tasks", response_model=Tasks)
# async def tasks(token: Annotated[str, Depends(oauth2_scheme)]):
#     return Tasks.from_obj()
