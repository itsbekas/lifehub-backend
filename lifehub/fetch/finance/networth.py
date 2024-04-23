from lifehub.clients.api import Trading212APIClient, YNABAPIClient
from lifehub.clients.db.finance import NetworthDBClient
from lifehub.fetch.base import BaseFetcher
from lifehub.models.finance import Networth


class NetworthFetcher(BaseFetcher):
    module_name = "networth"

    def fetch_data(self):
        ynab = YNABAPIClient(self.user.id)
        t212 = Trading212APIClient(self.user.id)

        ynab_accounts = ynab.get_accounts()
        t212_cash = t212.get_account_cash()

        bank_cash = round(sum([a.balance for a in ynab_accounts]), 2)
        uninvested_cash = round(t212_cash.free, 2)
        invested = round(t212_cash.invested, 2)
        returns = round(t212_cash.result, 2)
        total = bank_cash + uninvested_cash + invested + returns

        networth = Networth(
            bank_cash=bank_cash,
            uninvested_cash=uninvested_cash,
            invested=invested,
            returns=returns,
            total=total,
        )

        db = NetworthDBClient(self.user.id)

        db.add(networth)
