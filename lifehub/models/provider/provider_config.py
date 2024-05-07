from os import getenv

from sqlmodel import Field, SQLModel


def oauth_redirect_uri() -> str:
    return getenv("REDIRECT_URI_BASE") + "/account/oauth_token"


class BaseProviderConfig(SQLModel):
    provider_id: int = Field(primary_key=True, foreign_key="provider.id")
    allow_custom_url: bool = Field(default=False)


class OAuthProviderConfig(BaseProviderConfig, table=True):
    provider_id: int = Field(primary_key=True, foreign_key="provider.id")
    auth_url: str = Field(max_length=64, nullable=False)
    token_url: str = Field(max_length=64, nullable=False)
    client_id: str = Field(max_length=64, nullable=False)
    client_secret: str = Field(max_length=64, nullable=False)
    scope: str = Field(max_length=64, nullable=False)

    def build_auth_url(self) -> str:
        return f"{self.auth_url}?client_id={self.client_id}&redirect_uri={oauth_redirect_uri()}&scope={self.scope}&response_type=code&state={self.provider_id}"

    def build_token_url(self, auth_code: str) -> str:
        return f"{self.token_url}?client_id={self.client_id}&redirect_uri={oauth_redirect_uri()}&scope={self.scope}&grant_type=authorization_code&client_secret={self.client_secret}&code={auth_code}"

    def build_refresh_token_url(self, refresh_token: str) -> str:
        return f"{self.token_url}?client_id={self.client_id}&redirect_uri={oauth_redirect_uri()}&scope={self.scope}&grant_type=refresh_token&client_secret={self.client_secret}&refresh_token={refresh_token}"


class TokenProviderConfig(BaseProviderConfig, table=True):
    pass


class BasicProviderConfig(BaseProviderConfig, table=True):
    pass
