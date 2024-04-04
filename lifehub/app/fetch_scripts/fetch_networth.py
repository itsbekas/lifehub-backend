from dotenv import load_dotenv
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

    cash = sum([a.balance for a in accounts])

    if t212 is None:
        t212 = Trading212()

    investments = t212.get_account_cash().total

    networth = Networth(cash=round(cash, 2), investments=round(investments, 2))

    db_session.add(networth)
    db_session.commit()


if __name__ == "__main__":
    load_dotenv()

    ynab = YNAB()
    t212 = Trading212()

    with get_session() as db_session:
        fetch_networth(ynab, t212, db_session)

        db_session.close()
