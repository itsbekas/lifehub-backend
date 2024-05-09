from lifehub.clients.api import Trading212APIClient
from lifehub.core.base_fetcher import BaseFetcher
from lifehub.modules.finance.schema import T212Order, T212Transaction


class T212HistoryFetcher(BaseFetcher):
    module_name = "t212history"

    def fetch_data(self):
        t212 = Trading212APIClient(self.user)

        orders = t212.get_order_history()
        transactions = t212.get_transactions()

        for order in orders:
            if order.date_modified > self.prev_timestamp:
                quantity = order.filled_quantity

                if quantity is None:
                    quantity = order.filled_value / order.fill_price

                new_order = T212Order(
                    id=order.id,
                    user_id=self.user.id,
                    ticker=order.ticker,
                    quantity=quantity,
                    price=order.fill_price,
                    timestamp=order.date_modified,
                )
                self.session.add(new_order)

        for transaction in transactions:
            if transaction.date_time > self.prev_timestamp:
                new_transaction = T212Transaction(
                    id=transaction.reference,
                    user_id=self.user.id,
                    amount=transaction.amount,
                    timestamp=transaction.date_time,
                )
                self.session.add(new_transaction)
