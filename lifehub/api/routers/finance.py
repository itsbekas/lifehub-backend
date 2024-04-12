from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from lifehub.api.routers.dependencies import oauth2_scheme
from lifehub.lib.db import get_session
from lifehub.lib.models.finance import Networth

router = APIRouter(
    prefix="/finance",
    tags=["finance"],
)


@router.get("/networth", response_model=Networth)
async def networth(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_session),
):
    with session as s:
        query = select(Networth).order_by(Networth.timestamp.desc())
        networth = s.exec(query).first()

    return networth
