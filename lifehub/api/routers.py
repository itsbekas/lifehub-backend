from .auth.router import router as auth_router
from .finance.router import router as finance_router
from .server.router import router as server_router
from .tasks.router import router as tasks_router

__all__ = ["auth_router", "finance_router", "tasks_router", "server_router"]
