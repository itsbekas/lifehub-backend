from sqlmodel import Field, SQLModel


class Provider(SQLModel, table=True):
    name: str = Field(max_length=32, primary_key=True)
    type: str = Field(max_length=16)
