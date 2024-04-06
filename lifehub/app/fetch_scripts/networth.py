from lifehub.lib.api import YNAB, Trading212
from lifehub.lib.models.finance import Networth
from lifehub.app.fetch_scripts.fetch import Fetch

class NetworthFetch(Fetch):
    table_id = "networth_fetch"

    def fetch_data(self):
        ynab = YNAB.get_instance()
        t212 = Trading212.get_instance()

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

        self.session.add(networth)
