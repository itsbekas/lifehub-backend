import sys


def run():
    if len(sys.argv) < 2:
        raise ValueError("Please provide a fetch script to run")

    fetch_script = sys.argv[1]

    match fetch_script:
        case "t212history":
            from lifehub.app.fetchers.t212history import T212HistoryFetcher

            T212HistoryFetcher().fetch()
        case "networth":
            from lifehub.app.fetchers.networth import NetworthFetcher

            NetworthFetcher().fetch()
        case "qbitstats":
            from lifehub.app.fetchers.qbittorrent_stats import (
                QBittorrentStatsFetcher,
            )

            QBittorrentStatsFetcher().fetch()
        case _:
            raise ValueError(f"Fetch script {fetch_script} not found")


if __name__ == "__main__":
    run()
