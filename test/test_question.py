import pytest
from . import create_headers
from .test_auth import test_join

question = {
    'title': '이걸 모르겠어요',
    'article': '도와주세요ㅜㅜ 진짜 알다가도 모르겠습니다',
    'cartegory': '수학',
    'photo': 'https://via.placeholder.com/500x300'
}


async def test_question_post(test_cli):
    token = await test_join(test_cli)
    headers = create_headers(token)

    resp = await test_cli.post('/question/', headers=headers, json=question)
    assert resp.status == 200
    resp_json = await resp.json()
    question_id = resp_json['id']

    resp = await test_cli.get('/question/{}'.format(question_id), headers=headers)
    assert resp.status == 200
    resp_json = await resp.json()
    question_keys = [
        'id',
        'user_id',
        'title',
        'article',
        'cartegory',
        'photo',
        'status',
        'portfolio']
    for key in question_keys:
        assert key in resp_json

    return resp_json
