"""Lighting Gale api module interface

CONSTANTS:
    FMT_LG: LG datetime format
"""
from datetime import datetime
import json
import logging
from pathlib import Path
from typing import Union
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field
import requests

logger = logging.getLogger(__name__)

# Datetime format for LG
FMT_LG = '%a, %d %b %Y %H:%M:%S GMT'


class Token(BaseModel):
    access_token: str
    token_type: str  # bearer
    expires_in: int  # 43199
    issued: str = Field(..., alias=".issued")  # Tue, 25 Oct 2022 21:11:55 GMT
    expires: str = Field(..., alias=".expires")  # Wed, 26 Oct 2022 09:11:55 GMT
    clientName: str
    expirationDate: str  # 2020-03-31


class AuthResponse(BaseModel):
    token: Token
    status: int


class LGAuth:
    """LG Authentication related process.

    Attributes:
        auth_file: A path that reference a cache auth response.

    Args:
        username: LG username account
        password: LG password account
        base_url: API base URL
        ssl_verify: False for disable SSL warnings. LG use HTTP, less secure.
    """
    auth_file = Path('.tmp/lg_auth.json').resolve()

    def __init__(self, username: str, password: str,
                 base_url: str, ssl_verify) -> None:
        self.auth_file.parent.mkdir(exist_ok=True, parents=True)
        self.__username = username
        self.__password = password
        self.base_url = base_url
        self.ssl_verify = ssl_verify

    def get_auth_token(self) -> str:
        """Start process for getting token authentication.

        1. Verify if token in cache.
        2. Verify if cached token has valid expiration.
        3. Check if require renew token, requesting one to server, and save them.
        """
        auth_response = self.auth_load_token_from_stogare()
        if auth_response:
            renew_token = not self.check_token_expiration(auth_response)
        else:
            renew_token = True
        if renew_token:
            logger.debug('Token is been renewing...')
            auth_response = self.auth()
            self.auth_persisten_save(auth_response.dict(by_alias=True))
        return auth_response.token.access_token

    def auth_load_token_from_stogare(self) -> Union[AuthResponse, None]:
        """Load token from storage.

        Returns:
            AuthResponse: data from file if cached or
            None: if errors raised.
        """
        try:
            with open(self.auth_file, 'r') as j:
                data_ = json.load(j)
        except FileNotFoundError:
            data_ = None
        else:
            data_ = AuthResponse(**data_)
        return data_

    def auth(self) -> AuthResponse:
        """Make a request to authenticate against LG Platorm.

        In orden to adquire a Token and the token type is bearer. Generated
        from user and password.

        Returns:
            Authentication response with access_token and expiration.
        """
        url = self.base_url + '/GetToken'
        auth_headers = {
            'username': self.__username,
            'password': self.__password
        }
        response = requests.post(
            url, headers=auth_headers, verify=self.ssl_verify
        )
        try:
            _data = response.json()
        except Exception:
            raise
        # {"message": "User Name or Password is Invalid", "status": "-1"}
        if _data['status'] == -1:
            raise ValueError(_data['message'])
        response.raise_for_status()
        return AuthResponse(**_data)

    def auth_persisten_save(self, auth_data) -> None:
        """Save token in persisten storage as json."""
        self.auth_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.auth_file, 'w') as j:
            json.dump(auth_data, j)

    def check_token_expiration(self, auth_data: AuthResponse) -> bool:
        """Check if token is expired or not based on datetime.

        Args:
            auth_data: Token data (sent by server or serialized).

        Returns:
            True for valid token, false otherwise.
        """
        # GIVE extra seconds before expiration occurs
        THRESHOLD = 10
        _expires = auth_data.token.expires
        expires = datetime.strptime(_expires, FMT_LG).replace(
            tzinfo=ZoneInfo('UTC')
        )
        now = datetime.now().astimezone()
        elapsed = expires - now
        if elapsed.total_seconds() > THRESHOLD:
            valid = True
        else:
            valid = False
        return valid
