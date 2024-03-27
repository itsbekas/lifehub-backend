from fastapi import APIRouter
from lifehub.lib.finance import get_networth

router = APIRouter(
    prefix="/finance",
    tags=["finance"],
)

@router.get("/networth")
async def networth() -> float:
    return get_networth()
