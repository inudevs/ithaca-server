from sanic.exceptions import abort
from sanic.response import json as res_json
from sanic_openapi import doc
from sanic_jwt_extended import jwt_required
from sanic_jwt_extended.tokens import Token
from server.api.service import service_api
from bson import ObjectId
import time


@service_api.get('/<question_id>')
@jwt_required
@doc.summary('대화 조회')
async def ChatView(request, token: Token, question_id):
    user = token.jwt_identity

    # question_id로 question 쿼리, 상태 확인
    # question_id로 chat 쿼리, timestamp로 정렬해 반환
    pass


@service_api.post('/<question_id>')
@jwt_required
@doc.summary('대화 전송')
async def ChatPost(request, token: Token, question_id):
    user = token.jwt_identity
    question = await request.app.db.questions.find_one({
        '_id': ObjectId(question_id)
    })
    if not question:
        abort(404)
    if question['user_id'] == user['id']:
        # user is mentee
        sender = 'mentee'
    else:
        sender = 'mentor'

    # user_id로 sender 구하고, text 타입의 chat 만들어 저장
    chat = {
        'type': 'text',
        'question_id': question_id,
        'sender': sender,
        'message': request.json['message'],
        'timestamp': int(time.time())
    }
    res = await request.app.db.chats.insert_one(chat)
    if not res.acknowledged:
        abort(500)
    # TODO: 양측에게 알람
    return res_json({})


@service_api.delete('/<question_id>')
@jwt_required
@doc.summary('대화 종료')
async def ChatEnd(request, token: Token, question_id):
    user = token.jwt_identity

    # question_id의 status 변경
    # TODO: 양측에게 알람
    pass


@service_api.post('/request/teacher/<chat_id>')
@jwt_required
@doc.summary('선생님 리뷰 요청')
async def RequestTeacher(request, token: Token, question_id):
    user = token.jwt_identity

    # chat_id로 question_id 구할 수 있음
    pass


@service_api.post('/request/offline/<chat_id>')
@jwt_required
@doc.summary('오프라인 멘토링 요청')
async def RequestOffline(request, token: Token, question_id):
    user = token.jwt_identity

    # chat_id로 question_id 구할 수 있음
    pass
