from dotenv import load_dotenv
from .demo_app import main_demo


def main():
    load_dotenv()

    main_demo()


if __name__ == "__main__":
    main()
