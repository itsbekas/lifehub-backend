import requests
from fastapi import HTTPException


class OAuthTokenRequestFailedException(HTTPException):
    def __init__(self, response: requests.Response):
        super().__init__(response.status_code, response.text)


class NoTokenException(HTTPException):
    def __init__(self):
        super().__init__(404, "No token found")


class InvalidTokenException(HTTPException):
    def __init__(self):
        super().__init__(403, "Invalid token")
