from sqlmodel import Session

from lifehub.app.db import get_session
from lifehub.lib.api import YNAB, Trading212
from lifehub.lib.models.finance import Networth

from .utils import get_and_update_fetch_timestamp

NETWORTH_FETCH = "networth_fetch"


def fetch_networth(db_session: Session = None):
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

    db_session.add(networth)


if __name__ == "__main__":
    with get_session() as db_session:
        get_and_update_fetch_timestamp(db_session, NETWORTH_FETCH)

        fetch_networth(db_session)

        db_session.commit()
        db_session.close()
