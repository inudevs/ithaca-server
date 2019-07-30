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
async def MentoringApprove(request, question_id):
    pass


@mentor_api.get('/')
@doc.summary('멘토링 목록')
async def MentoringList(request):
    pass
