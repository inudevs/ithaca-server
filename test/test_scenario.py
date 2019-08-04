import pytest

users = [
    {
        'name': '테스트',
        'school': '한국디지털미디어고등학교',
        'grade': 1,
        'klass': 1,
        'number': 1,
        'photo': 'https://via.placeholder.com/128',
        'user_type': 'S',
        'email': 'test@example.com',
        'password': 'test'
    }, {
        'name': '스트테',
        'school': '한국디지털미디어고등학교',
        'grade': 1,
        'klass': 1,
        'number': 2,
        'photo': 'https://via.placeholder.com/128',
        'user_type': 'S',
        'email': 'hello@example.com',
        'password': 'test'
    }
]

class client:
    def __init__(self, user, test_cli):
        self.user = user
        self.cli = test_cli

    async def join(self):
        resp = await self.cli.post('/auth/join', json=self.user)
        assert resp.status in [200, 400]
    
    async def login(self):
        await self.join()
        resp = await self.cli.post('/auth/login', json={
            'email': self.user['email'],
            'password': self.user['password'],
        })
        assert resp.status in [200, 400]
        resp_json = await resp.json()
        assert 'token' in resp_json
        self.token = resp_json['token']


async def test_for_scenario(test_cli):
    client1 = client(users[0], test_cli)
    await client1.login()
    client2 = client(users[1], test_cli)
    await client2.login()

    # 회원가입 및 로그인 성공    
    assert client1.token
    assert client2.token

    # 클라1이 question 게시
    # 클라2가 question 목록을 통해 조회
    # 클라2가 question에 멘토링 request
    # 클라1이 클라2의 request를 approve
    # 클라1이 멘토링 리스트 조회, 채팅 보내기
    # 클라2가 채팅 받기
    # 클라2가 수식 전송
    # 클라1이 채팅 받기 
    # 클라1이 클라2의 메세지로 선생님 리뷰 요청
    # 클라2가 채팅 받기
    # 클라1이 채팅 종료
    # 클라이언트들이 멘토링 리스트 조회, 포트폴리오 출력
