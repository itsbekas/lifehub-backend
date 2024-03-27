class AccountCash:
    def __init__(
        self,
        blocked: float,
        free: float,
        invested: float,
        pieCash: float,
        ppl: float,
        result: float,
        total: float,
    ):
        self.blocked: float = blocked
        self.free: float = free
        self.invested: float = invested
        self.pieCash: float = pieCash
        self.ppl: float = ppl
        self.result: float = result
        self.total: float = total

    @classmethod
    def from_response(cls, data: dict):
        return cls(**data)

    def __repr__(self):
        return f"<Trading212 AccountCash: {self.total}>"


class AccountMetadata:
    def __init__(
        self,
        currencyCode: str,
        id: int,
    ):
        self.currencyCode: str = currencyCode
        self.id: int = id

    @classmethod
    def from_response(cls, data: dict):
        return cls(**data)

    def __repr__(self):
        return f"<Trading212 AccountMetadata: {self.id}>"
