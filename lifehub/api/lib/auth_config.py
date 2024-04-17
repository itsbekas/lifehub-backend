# Authentication types:
# - oauth2: OAuth 2.0, requires authorization, access token, and refresh token
# - token: Token-based authentication, requires a token
# - basic: Basic authentication, requires a username and password

auth_info = {
    "ynab": {
        "type": "oauth2",
        "authorization_url": "https://app.ynab.com/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code",
        "token_url": "https://app.ynab.com/oauth/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&redirect_uri={REDIRECT_URI}&grant_type=authorization_code&code={AUTHORIZATION_CODE}",
        "refresh_url": "https://app.ynab.com/oauth/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type=refresh_token&refresh_token={REFRESH_TOKEN}",
    },
    "trading212": {
        "type": "token",
    },
    "qbittorrent": {
        "type": "basic",
    },
}
