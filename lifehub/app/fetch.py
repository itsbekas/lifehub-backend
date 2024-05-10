import sys

from dotenv import load_dotenv


def run():
    if len(sys.argv) < 2:
        raise ValueError("Please provide a fetch script to run")

    fetch_script = sys.argv[1]

    load_dotenv()

    match fetch_script:
        case "t212history":
            from lifehub.providers.trading212.fetcher import T212HistoryFetcher

            T212HistoryFetcher().fetch()
        case "networth":
            from lifehub.providers.ynab.fetcher import NetworthFetcher

            NetworthFetcher().fetch()
        case "qbitstats":
            from lifehub.providers.qbittorrent.fetcher import (
                QBittorrentStatsFetcher,
            )

            QBittorrentStatsFetcher().fetch()
        case "all":
            from lifehub.providers.qbittorrent.fetcher import QBittorrentStatsFetcher
            from lifehub.providers.trading212.fetcher import T212HistoryFetcher
            from lifehub.providers.ynab.fetcher import NetworthFetcher

            T212HistoryFetcher().fetch()
            NetworthFetcher().fetch()
            QBittorrentStatsFetcher().fetch()
        case _:
            raise ValueError(f"Fetch script {fetch_script} not found")


if __name__ == "__main__":
    run()
