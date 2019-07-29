from sanic.exceptions import abort
from sanic.response import json as res_json
from sanic_openapi import doc
from server.api.question import question_api
from bson import ObjectId


@question_api.get('/')
@doc.summary('질문 목록')
async def QuestionList(request):
    pass


@question_api.post('/')
@doc.summary('질문 게시')
async def QuestionPost(request):
    pass


@question_api.get('/<question_id:ObjectId>')
@doc.summary('질문 조회')
async def QuestionView(request, question_id):
    pass
