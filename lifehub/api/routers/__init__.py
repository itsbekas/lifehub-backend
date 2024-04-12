from .finance import router as finance_router
from .server import router as server_router
from .tasks import router as tasks_router
from .user import router as auth_router

__all__ = ["auth_router", "finance_router", "tasks_router", "server_router"]
