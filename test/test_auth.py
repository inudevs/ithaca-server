import pytest

user = {
    'name': '테스트',
    'school': '한국디지털미디어고등학교',
    'grade': 1,
    'klass': 1,
    'number': 20,
    'photo': 'https://via.placeholder.com/128',
    'user_type': 'S',
    'email': 'test@example.com',
    'password': 'test'
}


async def test_join(test_cli):
    '''회원가입 테스트'''
    resp = await test_cli.post('/auth/join', json=user)
    assert resp.status in [
        200, # 성공
        400 # 이미 존재하는 사용자
    ]

    '''로그인 테스트'''
    resp = await test_cli.post('/auth/login', json={
        'email': user['email'],
        'password': user['password']
    })
    assert resp.status == 200
    resp_json = await resp.json()
    for key in ['token', 'refresh_token', 'user']:
        assert key in resp_json
