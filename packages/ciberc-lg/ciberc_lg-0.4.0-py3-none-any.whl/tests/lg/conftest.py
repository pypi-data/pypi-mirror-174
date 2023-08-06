from decouple import config
import pytest

from lg import LGApi, LGAuth


@pytest.fixture(scope='session')
def lg_auth() -> LGAuth:
    """Generate a session authenticated"""
    user = config('LG_USERNAME')
    passwd = config('LG_PASSWORD')
    base_url = config('LG_BASE_URL')
    return LGAuth(user, passwd, base_url, ssl_verify=False)


@pytest.fixture(scope='session')
def lg_api(lg_auth: LGAuth) -> LGApi:
    return LGApi(lg_auth)
