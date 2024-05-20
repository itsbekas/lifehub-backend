class ServiceException(Exception):
    def __init__(self, module: str, message: str) -> None:
        self.module = module
        self.message = message

    def __str__(self) -> str:
        return f"{self.module}: {self.message}"

    def __repr__(self) -> str:
        return f"<ServiceException({self.module}): {self.message}>"
