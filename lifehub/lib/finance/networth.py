from lifehub.lib.api import YNAB, Trading212, Habitica


def get_networth() -> float:
    ynab = YNAB()

    accounts = ynab.get_accounts()

    cash = 0

    for a in accounts:
        cash += a.balance

    t212 = Trading212()

    investments = t212.get_account_cash().total

    return {
        "cash": round(cash, 2),
        "investments": round(investments, 2),
        "total": round(cash + investments, 2),
    }
