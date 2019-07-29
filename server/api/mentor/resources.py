from sanic.exceptions import abort
from sanic.response import json as res_json
from sanic_openapi import doc
from server.api.mentor import mentor_api
from bson import ObjectId


@mentor_api.post('/request/<question_id:ObjectId>')
@doc.summary('멘토링 신청')
async def MentoringRequest(request, question_id):
    pass


@mentor_api.post('/approve/<question_id:ObjectId>')
@doc.summary('멘토링 승인')
async def MentoringApprove(request, question_id):
    pass


@mentor_api.get('/')
@doc.summary('멘토링 목록')
async def MentoringList(request):
    pass
