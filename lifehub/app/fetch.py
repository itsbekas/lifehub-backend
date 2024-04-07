import sys

from dotenv import load_dotenv


def run():
    if len(sys.argv) < 2:
        raise ValueError("Please provide a fetch script to run")

    fetch_script = sys.argv[1]

    load_dotenv()

    match fetch_script:
        case "t212history":
            from lifehub.fetch.finance.t212history import T212HistoryFetcher

            T212HistoryFetcher().fetch()
        case "networth":
            from lifehub.fetch.finance.networth import NetworthFetcher

            NetworthFetcher().fetch()
        case "qbitstats":
            from lifehub.fetch.server.qbittorrent_stats import (
                QBittorrentStatsFetcher,
            )

            QBittorrentStatsFetcher().fetch()
        case _:
            raise ValueError(f"Fetch script {fetch_script} not found")


if __name__ == "__main__":
    run()
