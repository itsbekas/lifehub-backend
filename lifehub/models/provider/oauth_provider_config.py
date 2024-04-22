from sqlmodel import Field, SQLModel


class OAuthProviderConfig(SQLModel, table=True):
    provider_id: int = Field(primary_key=True, foreign_key="provider.id")
    auth_url: str = Field(max_length=64, nullable=False)
    token_url: str = Field(max_length=64, nullable=False)
    client_id: str = Field(max_length=64, nullable=False)
    client_secret: str = Field(max_length=64, nullable=False)
    scope: str = Field(max_length=64, nullable=False)
    redirect_uri: str = Field(max_length=64, nullable=False)

    def build_auth_url(self) -> str:
        return f"{self.auth_url}?client_id={self.client_id}&redirect_uri={self.redirect_uri}&scope={self.scope}&response_type=code"

    def build_token_url(self, auth_code: str) -> str:
        return f"{self.token_url}?client_id={self.client_id}&client_secret={self.client_secret}&redirect_uri={self.redirect_uri}&scope={self.scope}&grant_type=authorization_code&code={auth_code}"

    def build_refresh_token_url(self, refresh_token: str) -> str:
        return f"{self.token_url}?client_id={self.client_id}&client_secret={self.client_secret}&redirect_uri={self.redirect_uri}&scope={self.scope}&grant_type=refresh_token&refresh_token={refresh_token}"
