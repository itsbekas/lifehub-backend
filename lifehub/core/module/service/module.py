from lifehub.core.common.base_service import BaseService
from lifehub.core.common.exceptions import ServiceException
from lifehub.core.module.models import ModuleResponse, ModuleWithProvidersResponse
from lifehub.core.module.repository.module import ModuleRepository
from lifehub.core.module.schema import Module
from lifehub.core.provider.models import ProviderResponse


class ModuleServiceException(ServiceException):
    def __init__(self, message: str):
        super().__init__("Module", message)


class ModuleService(BaseService):
    def __init__(self) -> None:
        super().__init__()
        self.module_repository = ModuleRepository(self.session)

    def get_modules(self) -> list[ModuleResponse]:
        modules = self.module_repository.get_all()

        return [
            ModuleResponse(
                id=module.id,
                name=module.name,
            )
            for module in modules
        ]

    def get_modules_with_providers(self) -> list[ModuleWithProvidersResponse]:
        modules = self.module_repository.get_all()

        return [
            ModuleWithProvidersResponse(
                id=module.id,
                name=module.name,
                providers=[
                    ProviderResponse(
                        id=provider.id,
                        name=provider.name,
                    )
                    for provider in module.providers
                ],
            )
            for module in modules
        ]

    def get_module_by_id(self, module_id: int) -> Module:
        module = self.module_repository.get_by_id(module_id)
        if module is None:
            raise ModuleServiceException("Module not found")
        return module
