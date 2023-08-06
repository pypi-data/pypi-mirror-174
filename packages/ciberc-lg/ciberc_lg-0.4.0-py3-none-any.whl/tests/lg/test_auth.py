from lg import LGAuth


def test_lg_auth(lg_auth: LGAuth):
    t = lg_auth.get_auth_token()
    assert isinstance(t, str)
