from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from lifehub.lib.finance import get_networth
from pydantic import BaseModel

router = APIRouter(
    prefix="/finance",
    tags=["finance"],
)


class Networth(BaseModel):
    total: float


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


@router.get("/networth", response_model=Networth)
async def networth(token: Annotated[str, Depends(oauth2_scheme)]):
    return Networth(total=get_networth())
