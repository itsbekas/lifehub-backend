from sqlmodel import Session

from lifehub.app.db import get_session
from lifehub.lib.api import YNAB, Trading212
from lifehub.models.finance import Networth


def fetch_networth(
    ynab: YNAB = None, t212: Trading212 = None, db_session: Session = None
):
    if ynab is None:
        ynab = YNAB()

    accounts = ynab.get_accounts()

    bank_cash = sum([a.balance for a in accounts])

    if t212 is None:
        t212 = Trading212()

    t212_cash = t212.get_account_cash()

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
    db_session.commit()


if __name__ == "__main__":
    ynab = YNAB()
    t212 = Trading212()

    with get_session() as db_session:
        fetch_networth(ynab, t212, db_session)

        db_session.close()
