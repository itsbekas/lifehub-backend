from typing import Annotated

from fastapi import Depends

from lifehub.core.user.api.dependencies import UserDep
from lifehub.modules.finance.service import FinanceService


def get_finance_service(user: UserDep) -> FinanceService:
    return FinanceService(user)


FinanceServiceDep = Annotated[FinanceService, Depends(get_finance_service)]
