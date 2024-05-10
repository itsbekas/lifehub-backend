import datetime as dt

from pydantic import BaseModel


class UserTokenResponse(BaseModel):
    name: str
    access_token: str
    expires_at: dt.datetime
