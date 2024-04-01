class MainData:
    def __init__(
        self,
        rid: int,
        full_update: bool,
        torrents: dict,
        categories: dict,
        tags: list[str],
        trackers: dict,
        server_state: dict,
    ):
        self.rid: int = rid
        self.full_update: bool = full_update
        self.torrents: dict = torrents  # TODO: Torrent model
        self.trackers: dict = trackers  # TODO: Tracker model
        self.categories: dict = categories  # TODO: Category model
        self.tags: list[str] = tags
        self.server_state: ServerState = ServerState.from_response(server_state)

    @classmethod
    def from_response(cls, data: dict):
        return cls(**data)


class ServerState:
    def __init__(
        self,
        alltime_dl: int,
        alltime_ul: int,
        average_time_queue: int,
        connection_status: str,
        dht_nodes: int,
        dl_info_data: int,
        dl_info_speed: int,
        dl_rate_limit: int,
        free_space_on_disk: int,
        global_ratio: str,
        queued_io_jobs: int,
        queueing: bool,
        read_cache_hits: str,
        read_cache_overload: str,
        refresh_interval: int,
        total_buffers_size: int,
        total_peer_connections: int,
        total_queued_size: int,
        total_wasted_session: int,
        up_info_data: int,
        up_info_speed: int,
        up_rate_limit: int,
        use_alt_speed_limits: bool,
        write_cache_overload: str,
    ):
        self.alltime_dl: int = alltime_dl
        self.alltime_ul: int = alltime_ul
        self.average_time_queue: int = average_time_queue
        self.connection_status: str = connection_status
        self.dht_nodes: int = dht_nodes
        self.dl_info_data: int = dl_info_data
        self.dl_info_speed: int = dl_info_speed
        self.dl_rate_limit: int = dl_rate_limit
        self.free_space_on_disk: int = free_space_on_disk
        self.global_ratio: float = float(global_ratio)
        self.queued_io_jobs: int = queued_io_jobs
        self.queueing: bool = queueing
        self.read_cache_hits: float = float(read_cache_hits)
        self.read_cache_overload: float = float(read_cache_overload)
        self.refresh_interval: int = refresh_interval
        self.total_buffers_size: int = total_buffers_size
        self.total_peer_connections: int = total_peer_connections
        self.total_queued_size: int = total_queued_size
        self.total_wasted_session: int = total_wasted_session
        self.up_info_data: int = up_info_data
        self.up_info_speed: int = up_info_speed
        self.up_rate_limit: int = up_rate_limit
        self.use_alt_speed_limits: bool = use_alt_speed_limits
        self.write_cache_overload: float = float(write_cache_overload)

    @classmethod
    def from_response(cls, data: dict):
        return cls(**data)
