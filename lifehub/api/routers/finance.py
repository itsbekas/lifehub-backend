from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from lifehub.api.routers.dependencies import get_user_id, get_session
from lifehub.models.finance import Networth
import uuid

router = APIRouter(
    prefix="/finance",
    tags=["finance"],
)


@router.get("/networth", response_model=Networth)
async def networth(
    user_id: Annotated[uuid.UUID, Depends(get_user_id)],
    session: Session = Depends(get_session),
):
    with session as s:
        query = select(Networth).order_by(Networth.timestamp.desc())
        networth = s.exec(query).first()

    return networth
