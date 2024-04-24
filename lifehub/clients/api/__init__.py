from .qbittorrent.qbittorrent import QBittorrentAPIClient
from .trading212.trading212 import Trading212APIClient
from .ynab.ynab import YNABAPIClient

__all__ = [
    "Trading212APIClient",
    "YNABAPIClient",
    "QBittorrentAPIClient",
]

api_clients = {
    "trading212": Trading212APIClient,
    "ynab": YNABAPIClient,
    "qbittorrent": QBittorrentAPIClient,
}
