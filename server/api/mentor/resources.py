from sanic.exceptions import abort
from sanic.response import json as res_json
from sanic_openapi import doc
from sanic_jwt_extended import jwt_required
from sanic_jwt_extended.tokens import Token
from server.api.mentor import mentor_api
from bson import ObjectId
import time


@mentor_api.post('/request/<question_id>')
@jwt_required
@doc.summary('멘토링 신청')
async def MentoringRequest(request, token: Token, question_id):
    user = token.jwt_identity

    # 이미 신청한 멘토링은 아닌지 확인
    if await request.app.db.requests.find_one({
        'user_id': user['id'],
        'question_id': question_id,
    }):
        abort(400)

    req = {
        'user_id': user['id'],
        'question_id': question_id,
        'timestamp': int(time.time()),
        'approved': False
    }
    res = await request.app.db.requests.insert_one(req)
    if not res.acknowledged:
        abort(500)
    return res_json({'id': str(res.inserted_id)})


@mentor_api.post('/approve/<question_id>')
@doc.summary('멘토링 승인')
async def MentoringApprove(request, token: Token, question_id):
    user = token.jwt_identity

    # question 쿼리, 작성자 확인
    question = await request.app.db.requests.find_one({
        'user_id': user['id'],
        'question_id': question_id,
    })
    if not question:
        abort(404)

    # 다른 멘토링이 이미 승인된 것은 아닌지 확인
    if await request.app.db.requests.find_one({
        'question_id': question_id,
        'approved': True
    }):
        abort(400)

    # post로 받은 request_id를 가진 request의 approved를 True로 업데이트
    request_id = request.json['request_id']
    res = await request.app.db.requests.update_one({'_id': ObjectId(request_id)}, {
        '$set': {
            'approved': True
        }
    })
    if not res.acknowledged:
        abort(500)

    # question의 status 변경
    res = await request.app.db.questions.update_one({'_id': ObjectId(question_id)}, {
        '$set': {
            'status': 'M'
        }
    })
    if not res.acknowledged:
        abort(500)

    return res_json({})


@mentor_api.get('/')
@doc.summary('멘토링 목록')
async def MentoringList(request):
    pass
