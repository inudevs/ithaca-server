import pytest


async def test_school_autocomplete(test_cli):
    # deprecated
    return

    async def check_resp(query, result):
        resp = await test_cli.get('/search/school/{}'.format(query))
        assert resp.status == 200
        resp_json = await resp.json()
        assert resp_json == result

    await check_resp('한국디', ['한국디지털미디어고등학교'])
    await check_resp('정발', ['정발고등학교', '정발중학교', '정발초등학교'])
