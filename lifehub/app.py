from dotenv import load_dotenv
from lifehub.api.ynab import YNAB
from lifehub.api.trading212 import Trading212


def main():
    load_dotenv()

    ynab = YNAB()

    accounts = ynab.get_accounts()

    total_balance = 0

    for a in accounts:
        print(f"{a.name}: {a.balance}")
        total_balance += a.balance

    t212 = Trading212()

    account = t212.get_account()

    print(f"Trading212: {account['total']}")
    total_balance += account["total"]

    print("")

    print(f"Total: {round(total_balance, 2)}")


if __name__ == "__main__":
    main()
