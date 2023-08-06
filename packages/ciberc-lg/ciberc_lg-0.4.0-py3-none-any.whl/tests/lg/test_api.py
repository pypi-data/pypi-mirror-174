from lg import LGApi


def test_get_all_slcs(lg_api: LGApi):
    assert bool(lg_api.get_all_slcs())
