from typing import Annotated

from fastapi import APIRouter, Depends

from ..auth.lib import oauth2_scheme
from .lib import get_tasks
from .schemas import Tasks

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.get("/tasks", response_model=Tasks)
async def tasks(token: Annotated[str, Depends(oauth2_scheme)]):
    return Tasks.from_obj(**get_tasks())
