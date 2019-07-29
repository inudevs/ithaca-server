from sanic.exceptions import abort
from sanic.response import json as res_json
from sanic_openapi import doc
from sanic_jwt_extended import jwt_required
from sanic_jwt_extended.tokens import Token
from server.api.question import question_api
from server.api.question.models import *
from bson import ObjectId


@question_api.get('/')
@jwt_required
@doc.summary('질문 목록')
async def QuestionList(request, token: Token):
    pass


@question_api.post('/')
@jwt_required
@doc.summary('질문 게시')
@doc.consumes(
    CreateQuestionModel,
    content_type='application/json',
    location='body')
@doc.response(200, None, description='성공')
async def QuestionPost(request, token: Token):
    user = token.jwt_identity
    question = {
        'user_id': user['id'],
        'requests': [],
        'status': 'P',
        'portfolio': None
    }
    keys = ['title', 'article', 'cartegory', 'photo']
    for key in keys:
        question[key] = request.json[key]
    res = await request.app.db.questions.insert_one(question)
    if not res.acknowledged:
        abort(500)
    return res_json({'id': str(res.inserted_id)})


@question_api.get('/<question_id>')
@jwt_required
@doc.response(200, None, description='성공')
@doc.summary('질문 조회')
async def QuestionView(request, token: Token, question_id):
    question = await request.app.db.questions.find_one({
        '_id': ObjectId(question_id)
    })
    if not question:
        abort(404)
    question['id'] = str(question['_id'])
    del question['_id']
    for idx, req in enumerate(question['requests']):
        question['requests'][idx]['id'] = str(req['_id'])
        # TODO: remove more fields
    return res_json(question)
