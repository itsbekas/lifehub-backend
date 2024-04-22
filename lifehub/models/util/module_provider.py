from sqlmodel import Field, SQLModel


class ModuleProvider(SQLModel, table=True):
    module_id: int = Field(foreign_key="module.id", primary_key=True)
    provider_id: int = Field(foreign_key="provider.id", primary_key=True)
