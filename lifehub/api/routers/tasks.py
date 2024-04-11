from fastapi import APIRouter
from sqlmodel import Session, select

# from lifehub.lib.models.tasks import Task
from typing import Annotated
from fastapi import Depends
from lifehub.api.auth.lib import oauth2_scheme

tasks_router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


# @tasks_router.get("/tasks", response_model=Tasks)
# async def tasks(token: Annotated[str, Depends(oauth2_scheme)]):
#     return Tasks.from_obj()
