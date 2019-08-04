import pytest

user_data = [
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

question_data = {
    'title': '이걸 모르겠어요',
    'article': '도와주세요ㅜㅜ 진짜 알다가도 모르겠습니다',
    'cartegory': '수학',
    'photo': 'https://via.placeholder.com/500x300'
}

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
        self.headers = {
            'authorization': 'Bearer {}'.format(self.token),
            'content-type': 'application/json'
        }
    
    async def request(self, method, url, data={}):
        resp = await method(url, headers=self.headers, json=data)
        resp_json = await resp.json()
        return resp.status, resp_json


async def test_for_scenario(test_cli):
    client1 = client(user_data[0], test_cli)
    await client1.login()
    client2 = client(user_data[1], test_cli)
    await client2.login()

    # 회원가입 및 로그인 성공    
    assert client1.token
    assert client2.token

    # 클라1이 question 게시
    resp_status, resp_json = await client1.request(test_cli.post, '/question/', question_data)
    assert resp_status == 200
    assert 'id' in resp_json # 생성된 question의 id
    question_id = resp_json['id']

    # 클라2가 question 목록을 통해 조회
    resp_status, resp_json = await client2.request(test_cli.get, '/question/')
    assert resp_status == 200
    assert 'questions' in resp_json
    for question in resp_json['questions']:
        if question_id == question['id']:
            assert question['status'] == 'P'
                # status가 pending
            print(question)
    
    # 클라2가 question에 멘토링 request
    resp_status, resp_json = await client2.request(test_cli.post, '/mentor/request/{}'.format(question_id))
    assert resp_status == 200
    assert 'id' in resp_json # 생성된 request의 id
    request_id = resp_json['id']

    # 클라1이 자신의 question을 조회해 request 목록 살핌
    resp_status, resp_json = await client1.request(test_cli.get, '/question/{}'.format(question_id))
    assert resp_status == 200
    assert 'requests' in resp_json
    for request in resp_json['requests']:
        if request_id == request['id']:
            print(request)

    # 클라1이 클라2의 request를 approve
    resp_status, _ = await client1.request(test_cli.post, '/mentor/approve/{}'.format(question_id), {
        'request_id': request_id
    })
    assert resp_status == 200

    # question의 status가 변경됬는지 확인
    resp_status, resp_json = await client1.request(test_cli.get, '/question/{}'.format(question_id))
    assert resp_status == 200
    assert resp_json['status'] == 'M'
        # question의 상태 변경됨
    assert resp_json['requests'][0]['approved'] == True
        # 멘토링 request가 승인됨

    # 클라1이 멘토링 리스트 조회
    resp_status, resp_json = await client1.request(test_cli.get, '/mentor/')
    assert resp_status == 200
    # assert 'mentorings' in resp_json
    # assert any(key in resp_json['mentorings'] for key in ['mentor', 'mentee'])
    # assert len(resp_json['mentorings']['mentor']) == 0 # 얘는 질문만 올려서 멘티만 함

    # 클라2이 멘토링 리스트 조회
    resp_status, resp_json = await client2.request(test_cli.get, '/mentor/')
    assert resp_status == 200
    # assert 'mentorings' in resp_json
    # assert any(key in resp_json['mentorings'] for key in ['mentor', 'mentee'])
    # assert len(resp_json['mentorings']['mentee']) == 0 # 얘는 멘토링만 해줘서 멘토만 함

    # 클라1이 대화 조회
    resp_status, resp_json = await client1.request(test_cli.get, '/service/{}'.format(question_id))
    assert resp_status == 200
    # assert 'chats' in resp_json
    # assert len(resp_json['chats']) == 0
    print(resp_json)

    # 클라1이 채팅 보내기
    resp_status, _ = await client1.request(test_cli.post, '/service/{}'.format(question_id), {
        'message': '안녕!'
    })
    assert resp_status == 200

    # 클라2가 채팅 보내기
    resp_status, _ = await client2.request(test_cli.post, '/service/{}'.format(question_id), {
        'message': '우웅 나도 안뇽!!'
    })
    assert resp_status == 200

    # 클라2가 채팅 확인
    resp_status, resp_json = await client2.request(test_cli.get, '/service/{}'.format(question_id))
    assert resp_status == 200
    print(resp_json)
    # ascending 순서가 맞는지도 체크해주자
    # 나중에 생성된 게 뒤에 있는 거.. 일껄!!

    # 클라2가 수식 전송
    # 클라1이 채팅 받기 
    # 클라1이 클라2의 메세지로 선생님 리뷰 요청
    # 클라2가 채팅 받기
    # 클라1이 채팅 종료
    # 둘 다 피드백 업로드
    # 클라이언트들이 멘토링 리스트 조회, 포트폴리오 출력
