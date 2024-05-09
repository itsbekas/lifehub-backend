import datetime as dt


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


class Order:
    def __init__(
        self,
        type: str,
        id: int,
        fillId: int,
        parentOrder: int,
        ticker: str,
        orderedQuantity: float | None,
        filledQuantity: float | None,
        limitPrice: float | None,
        stopPrice: float | None,
        timeValidity: None,
        orderedValue: float | None,
        filledValue: float | None,
        executor: str,
        dateModified: str,
        dateExecuted: str | None,
        dateCreated: str,
        fillResult: None,
        fillPrice: float | None,
        fillCost: float | None,
        taxes: list,
        fillType: str,
        status: str,
    ):
        self.type: str = type
        self.id: int = id
        self.fill_id: int = fillId
        self.parent_order: int = parentOrder
        self.ticker: str = ticker
        self.ordered_quantity: float | None = orderedQuantity
        self.filled_quantity: float | None = filledQuantity
        self.limit_price: float | None = limitPrice
        self.stop_price: float | None = stopPrice
        self.time_validity: None = timeValidity
        self.ordered_value: float | None = orderedValue
        self.filled_value: float | None = filledValue
        self.executor: str = executor
        self.date_modified: dt.datetime = dt.datetime.strptime(
            dateModified, "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        self.date_executed: dt.datetime | None = (
            dt.datetime.strptime(dateExecuted, "%Y-%m-%dT%H:%M:%S.%fZ")
            if dateExecuted is not None
            else None
        )
        self.date_created: dt.datetime = dt.datetime.strptime(
            dateCreated, "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        self.fill_result: None = fillResult
        self.fill_price: float | None = fillPrice
        self.fill_cost: float | None = fillCost
        self.taxes: list = taxes
        self.fill_type: str = fillType
        self.status: str = status

    @classmethod
    def from_response(cls, data: dict):
        return cls(**data)

    def __repr__(self):
        return f"<Trading212 Order: {self.id}>"


class Transaction:
    def __init__(
        self,
        type: str,
        amount: float,
        reference: str,
        dateTime: str,
    ):
        self.type: str = type
        self.amount: float = amount
        self.reference: str = reference
        self.date_time: dt.datetime = dt.datetime.strptime(
            dateTime, "%Y-%m-%dT%H:%M:%S.%fZ"
        )

    @classmethod
    def from_response(cls, data: dict):
        return cls(**data)

    def __repr__(self):
        return f"<Trading212 Transaction: {self.reference}>"
