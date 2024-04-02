from pydantic import BaseModel


class Networth(BaseModel):
    cash: float
    investments: float
