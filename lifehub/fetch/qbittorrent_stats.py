from lifehub.fetch.base_fetcher import BaseFetcher
from lifehub.lib.api import QBittorrent
from lifehub.lib.models.server import QBittorrentStats


class QBittorrentStatsFetcher(BaseFetcher):
    table_id = "qbit_stats_fetch"

    def fetch_data(self):
        qb = QBittorrent.get_instance()

        main_data = qb.get_main_data()

        state = main_data.server_state

        stats = QBittorrentStats(
            alltime_dl=state.alltime_dl,
            alltime_ul=state.alltime_ul,
            alltime_ratio=state.global_ratio,
        )

        self.session.add(stats)
