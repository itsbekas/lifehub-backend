from lifehub.lib.api import YNAB, Trading212


def get_networth(ynab: YNAB = YNAB(), t212: Trading212 = Trading212()) -> float:
    accounts = ynab.get_accounts()

    cash = 0

    for a in accounts:
        cash += a.balance

    investments = t212.get_account_cash().total

    return {
        "cash": round(cash, 2),
        "investments": round(investments, 2),
        "total": round(cash + investments, 2),
    }
