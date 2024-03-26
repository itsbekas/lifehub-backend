from dotenv import load_dotenv
from lifehub.api.ynab import YNAB


def main():
    load_dotenv()

    ynab = YNAB()

    accounts = ynab.get_accounts()

    for a in accounts:
        print(f"{a.name}: {a.balance}")


if __name__ == "__main__":
    main()
