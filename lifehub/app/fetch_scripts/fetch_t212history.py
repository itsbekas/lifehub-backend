import datetime as dt

from sqlmodel import Session, select

from lifehub.app.db import get_session
from lifehub.lib.api import Trading212
from lifehub.models.finance import T212Order, T212Transaction
from lifehub.models.utils import FetchUpdate

T212HISTORY_FETCH = "t212history_fetch"


def fetch_t212history(
    t212: Trading212 = None,
    db_session: Session = None,
    last_update: dt.datetime = dt.datetime.min,
):
    if t212 is None:
        t212 = Trading212()

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
    t212 = Trading212()

    with get_session() as db_session:
        current_time = dt.datetime.now()

        query = select(FetchUpdate).where(FetchUpdate.id == T212HISTORY_FETCH)

        res = db_session.exec(query).first()

        if res is None:  # TODO: Setup a default value on table creation
            last_update = dt.datetime.min
        else:
            last_update = res.last_update

        fetch_t212history(t212, db_session, last_update)

        res.last_update = current_time
        db_session.add(res)

        db_session.commit()
        db_session.close()
