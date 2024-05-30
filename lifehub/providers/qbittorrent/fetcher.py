from lifehub.providers.base.base_fetcher import BaseFetcher
from lifehub.providers.qbittorrent.api_client import QBittorrentAPIClient
from lifehub.providers.qbittorrent.schema import QBittorrentStats


class QBittorrentStatsFetcher(BaseFetcher):
    module_name = "qbittorrent"

    def fetch_data(self):
        qb = QBittorrentAPIClient.get_instance()

        main_data = qb.get_main_data()

        state = main_data.server_state

        stats = QBittorrentStats(
            alltime_dl=state.alltime_dl,
            alltime_ul=state.alltime_ul,
            alltime_ratio=state.global_ratio,
        )

        self.session.add(stats)
