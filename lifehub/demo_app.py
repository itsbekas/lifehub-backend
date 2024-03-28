from lifehub.lib.api import YNAB, Trading212, Habitica


def cash_demo():
    ynab = YNAB()

    accounts = ynab.get_accounts()

    total_balance = 0

    for a in accounts:
        print(f"{a.name}: {a.balance}")
        total_balance += a.balance

    t212 = Trading212()

    account_cash = t212.get_account_cash()

    print(f"Trading212: {account_cash.total}")
    total_balance += account_cash.total

    print("")

    print(f"Total: {round(total_balance, 2)}")


def tasks_demo():
    habitica = Habitica()

    # tasks = habitica.get_user_dailies()
    # tasks = habitica.get_user_habits()
    tasks = habitica.get_user_todos()

    print(tasks)


def main_demo():
    cash_demo()
    print("")
    tasks_demo()
