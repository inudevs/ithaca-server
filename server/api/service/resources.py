from sanic.exceptions import abort
from sanic.response import json as res_json
from sanic_openapi import doc
from server.api.service import service_api
from bson import ObjectId


@service_api.get('/<question_id>')
@doc.summary('대화 조회')
async def DialogueView(request, question_id):
    pass


@service_api.post('/<question_id>')
@doc.summary('대화 전송')
async def DialoguePost(request, question_id):
    pass


@service_api.delete('/<question_id>')
@doc.summary('대화 종료')
async def DialogueEnd(request, question_id):
    pass


@service_api.post('/request/teacher/<dialogue_id>')
@doc.summary('선생님 리뷰 요청')
async def RequestTeacher(request, question_id):
    pass


@service_api.post('/request/offline/<dialogue_id>')
@doc.summary('오프라인 멘토링 요청')
async def RequestOffline(request, question_id):
    pass
