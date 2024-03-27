from fastapi import APIRouter
from lifehub.lib.finance import get_networth
from pydantic import BaseModel

router = APIRouter(
    prefix="/finance",
    tags=["finance"],
)

class Networth(BaseModel):
    total: float

@router.get("/networth")
async def networth() -> Networth:
    return Networth(total=get_networth())
