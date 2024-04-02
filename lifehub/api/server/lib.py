from lifehub.lib.api import QBittorrent
from lifehub.lib.api.qbittorrent.models import ServerState


def get_qbit_server_state(qbittorrent: QBittorrent = None) -> ServerState:
    if qbittorrent is None:
        qbittorrent = QBittorrent()

    return qbittorrent.get_main_data().server_state
