from lifehub.lib.api import YNAB, Trading212, Habitica


def get_networth() -> float:
    ynab = YNAB()

    accounts = ynab.get_accounts()

    total_balance = 0

    for a in accounts:
        total_balance += a.balance

    t212 = Trading212()

    account_cash = t212.get_account_cash()

    total_balance += account_cash.total

    total_rounded: float = round(total_balance, 2)

    return total_rounded
