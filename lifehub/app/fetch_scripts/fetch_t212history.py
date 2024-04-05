import datetime as dt

from sqlmodel import Session

from lifehub.app.db import get_session
from lifehub.lib.api import Trading212
from lifehub.lib.models.finance import T212Order, T212Transaction

from .utils import get_and_update_fetch_timestamp

T212HISTORY_FETCH = "t212history_fetch"


def fetch_t212history(
    db_session: Session = None,
    last_update: dt.datetime = dt.datetime.min,
):
    t212 = Trading212.get_instance()

    orders = t212.get_order_history()
    transactions = t212.get_transactions()

    for order in orders:
        if order.date_modified > last_update:
            quantity = order.filled_quantity

            if quantity is None:
                quantity = order.filled_value / order.fill_price

            new_order = T212Order(
                type=order.type,
                id=order.id,
                ticker=order.ticker,
                quantity=quantity,
                price=order.fill_price,
                timestamp=order.date_modified,
            )
            db_session.add(new_order)

    for transaction in transactions:
        if transaction.date_time > last_update:
            new_transaction = T212Transaction(
                type=transaction.type,
                amount=transaction.amount,
                id=transaction.reference,
                timestamp=transaction.date_time,
            )
            db_session.add(new_transaction)


if __name__ == "__main__":
    with get_session() as db_session:
        last_update = get_and_update_fetch_timestamp(db_session, T212HISTORY_FETCH)

        fetch_t212history(db_session, last_update)

        db_session.commit()
        db_session.close()
