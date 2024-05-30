from lifehub.providers.base.base_fetcher import BaseFetcher
from lifehub.providers.trading212.api_client import Trading212APIClient
from lifehub.providers.trading212.schema import T212Balance, T212Order, T212Transaction


class Trading212Fetcher(BaseFetcher):
    provider_name = "trading212"

    def fetch_data(self) -> None:
        t212 = Trading212APIClient(self.user)

        orders = t212.get_order_history()
        transactions = t212.get_transactions()
        balance = t212.get_account_cash()

        for order in orders:
            if order.date_modified > self.prev_timestamp:
                quantity = order.filled_quantity

                if quantity is None:
                    if order.fill_price is None or order.filled_value is None:
                        continue
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

        if balance:
            new_balance = T212Balance(
                user_id=self.user.id,
                free=balance.free,
                invested=balance.invested,
                result=balance.result,
            )
            self.session.add(new_balance)
