from lifehub.clients.api import Trading212APIClient
from lifehub.fetch.base import BaseFetcher
from lifehub.models.finance import T212Order, T212Transaction


class T212HistoryFetcher(BaseFetcher):
    module_name = "t212history"

    def fetch_data(self):
        t212 = Trading212APIClient.get_instance()

        orders = t212.get_order_history()
        transactions = t212.get_transactions()

        for order in orders:
            if order.date_modified > self.last_update:
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
                self.session.add(new_order)

        for transaction in transactions:
            if transaction.date_time > self.last_update:
                new_transaction = T212Transaction(
                    type=transaction.type,
                    amount=transaction.amount,
                    id=transaction.reference,
                    timestamp=transaction.date_time,
                )
                self.session.add(new_transaction)
