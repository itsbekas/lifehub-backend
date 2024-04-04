from lifehub.lib.api import YNAB, Trading212


def get_networth(ynab: YNAB = None, t212: Trading212 = None):
    if ynab is None:
        ynab = YNAB()

    accounts = ynab.get_accounts()

    cash = 0

    for a in accounts:
        cash += a.balance

    if t212 is None:
        t212 = Trading212()

    investments = t212.get_account_cash().total

    return {"cash": round(cash, 2), "investments": round(investments, 2)}
