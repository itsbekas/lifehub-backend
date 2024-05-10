from lifehub.core.common.base_service import BaseService
from lifehub.core.module.models import ModuleResponse, ModuleWithProvidersResponse
from lifehub.core.module.repository.module import ModuleRepository
from lifehub.core.module.schema import Module
from lifehub.core.provider.models import ProviderResponse


class ModuleService(BaseService):
    def __init__(self):
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
        return self.module_repository.get_by_id(module_id)
