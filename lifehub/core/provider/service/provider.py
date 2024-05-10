from lifehub.core.common.base_service import BaseService
from lifehub.core.provider.models import ProviderResponse
from lifehub.core.provider.repository.provider import ProviderRepository
from lifehub.core.provider.schema import Provider


class ProviderService(BaseService):
    def __init__(self):
        super().__init__()
        self.provider_repository = ProviderRepository(self.session)

    def get_providers(self) -> list[ProviderResponse]:
        providers = self.provider_repository.get_all()

        return [
            ProviderResponse(
                id=provider.id,
                name=provider.name,
            )
            for provider in providers
        ]

    def get_provider_by_id(self, provider_id: int) -> Provider:
        return self.provider_repository.get_by_id(provider_id)
