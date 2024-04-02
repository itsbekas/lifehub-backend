from typing import Annotated

from fastapi import APIRouter, Depends

from lifehub.api.auth.lib import oauth2_scheme

from .lib import get_networth
from .schemas import Networth

router = APIRouter(
    prefix="/finance",
    tags=["finance"],
)


@router.get("/networth", response_model=Networth)
async def networth(token: Annotated[str, Depends(oauth2_scheme)]):
    return Networth(**get_networth())
