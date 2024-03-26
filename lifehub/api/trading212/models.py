class AccountCash:
    def __init__(
        self,
        blocked: int,
        free: int,
        invested: int,
        pieCash: int,
        ppl: int,
        result: int,
        total: int,
    ):
        self.blocked: int = blocked
        self.free: int = free
        self.invested: int = invested
        self.pieCash: int = pieCash
        self.ppl: int = ppl
        self.result: int = result
        self.total: int = total

    @classmethod
    def from_response(cls, data: dict):
        return cls(**data)

    def __repr__(self):
        return f"<Trading212 AccountCash: {self.total}>"
