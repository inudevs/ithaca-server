from sanic.exceptions import abort
from sanic.response import json as res_json
from sanic_openapi import doc
from sanic_jwt_extended import jwt_required
from sanic_jwt_extended.tokens import Token
from server.api.question import question_api
from server.api.question.models import *
from bson import ObjectId
import pymongo
import time


@question_api.get('/')
@jwt_required
@doc.summary('질문 목록')
async def QuestionList(request, token: Token):
    page = request.args.get('page') or 1
    per_page = request.args.get('per_page') or 10
    query = {
        'status': request.args.get('status') or 'P',
        'category': request.args.get('category')
    }
    if not query['category']:
        del query['category']
    cursor = request.app.db.questions.find({
    }).sort(
        'timestamp', pymongo.ASCENDING
    ).skip(
        (page - 1) * per_page
    ).limit(per_page)
    questions = await cursor.to_list(length=50)
    for question in questions:
        question['id'] = str(question['_id'])
        del question['_id']
        question['user'] = await request.app.db.users.find_one({
            '_id': ObjectId(question['user_id'])
        }, {'_id': False})
        del question['user_id']
        cursor = request.app.db.requests.find({
            'question_id': question['id']
        }, {'_id': False})
        question['requests'] = await cursor.to_list(length=50)
    return res_json({ 'questions': questions })


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
        'status': 'P',
        'portfolio': None,
        'timestamp': int(time.time())
    }
    keys = ['title', 'article', 'category', 'photo']
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
    }, {'_id':False})
    if not question:
        abort(404)
    question['id'] = question_id
    cursor = request.app.db.requests.find({
        'question_id': question_id
    })
    question['requests'] = await cursor.to_list(length=50)
    for idx, req in enumerate(question['requests']):
        question['requests'][idx]['id'] = str(req['_id'])
        del question['requests'][idx]['_id']
    # TODO: fix this
    return res_json(question)
