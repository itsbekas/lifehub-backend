import sys

from dotenv import load_dotenv


def run():
    if len(sys.argv) < 2:
        raise ValueError("Please provide a fetch script to run")

    fetch_script = sys.argv[1]

    load_dotenv()

    match fetch_script:
        case "t212history":
            from lifehub.modules.t212history.fetcher import T212HistoryFetcher

            T212HistoryFetcher().fetch()
        case "networth":
            from lifehub.modules.finance.fetcher import NetworthFetcher

            NetworthFetcher().fetch()
        case "qbitstats":
            from lifehub.modules.server.fetcher import (
                QBittorrentStatsFetcher,
            )

            QBittorrentStatsFetcher().fetch()
        case "all":
            from lifehub.modules.finance.fetcher import NetworthFetcher
            from lifehub.modules.server.fetcher import QBittorrentStatsFetcher
            from lifehub.modules.t212history.fetcher import T212HistoryFetcher

            T212HistoryFetcher().fetch()
            NetworthFetcher().fetch()
            QBittorrentStatsFetcher().fetch()
        case _:
            raise ValueError(f"Fetch script {fetch_script} not found")


if __name__ == "__main__":
    run()
