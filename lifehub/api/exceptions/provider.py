from fastapi import HTTPException, status


class ProviderExistsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Provider already exists",
        )


class ProviderDoesNotExistException(HTTPException):
    def __init__(self, provider_name: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Provider {provider_name} does not exist",
        )


class ProviderDetailsIncompleteException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provider details are incomplete",
        )


class ProviderTypeInvalidException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provider type is invalid",
        )
