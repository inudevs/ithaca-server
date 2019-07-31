from sanic.exceptions import abort
from sanic.response import json as res_json
from sanic_openapi import doc
from server.api.service import service_api
from bson import ObjectId


@service_api.get('/<question_id>')
@doc.summary('대화 조회')
async def ChatView(request, question_id):
    # question_id로 question 쿼리, 상태 확인
    # question_id로 chat 쿼리, timestamp로 정렬해 반환
    pass


@service_api.post('/<question_id>')
@doc.summary('대화 전송')
async def ChatPost(request, question_id):
    # user_id로 sender 구하고, text 타입의 chat 만들어 저장
    # TODO: 양측에게 알람
    pass


@service_api.delete('/<question_id>')
@doc.summary('대화 종료')
async def ChatEnd(request, question_id):
    # question_id의 status 변경
    # TODO: 양측에게 알람
    pass


@service_api.post('/request/teacher/<chat_id>')
@doc.summary('선생님 리뷰 요청')
async def RequestTeacher(request, question_id):
    # chat_id로 question_id 구할 수 있음
    pass


@service_api.post('/request/offline/<chat_id>')
@doc.summary('오프라인 멘토링 요청')
async def RequestOffline(request, question_id):
    # chat_id로 question_id 구할 수 있음
    pass
