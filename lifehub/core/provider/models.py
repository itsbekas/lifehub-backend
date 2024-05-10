from pydantic.dataclasses import dataclass


@dataclass
class ProviderResponse:
    id: int
    name: str
    # modules: List[ModuleResponse]
