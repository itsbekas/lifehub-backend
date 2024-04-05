from sqlmodel import Session

from lifehub.app.db import get_session
from lifehub.lib.api import Trading212
from lifehub.models.finance import T212Order, T212Transaction


def fetch_t212transactions(t212: Trading212 = None, db_session: Session = None):
    if t212 is None:
        t212 = Trading212()

    orders = t212.get_order_history()
    transactions = t212.get_transactions()

    for order in orders:
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
        fetch_t212transactions(t212, db_session)

        db_session.commit()
        db_session.close()
