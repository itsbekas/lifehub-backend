from pydantic import BaseModel

from lifehub.lib.api.qbittorrent.models import ServerState


class AllTimeStats(BaseModel):
    dl: int
    ul: int
    ratio: float

    @classmethod
    def from_obj(cls, state: ServerState):
        return cls(dl=state.alltime_dl, ul=state.alltime_ul, ratio=state.global_ratio)
