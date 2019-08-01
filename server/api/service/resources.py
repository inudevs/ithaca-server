from sanic.exceptions import abort
from sanic.response import json as res_json
from sanic_openapi import doc
from sanic_jwt_extended import jwt_required
from sanic_jwt_extended.tokens import Token
from server import sio
from server.api.service import service_api
import pymongo
from bson import ObjectId
import time

# 1. 사용자 채팅 접속 시 question_id로 client.emit
# 2. 메세지를 보낼 때 question_id의 room에 서버가 뭔가를 emit
#   -> client.on('something') 시 채팅이 업데이트 되었다는 것 -> reload
# (프로토타입이므로 원시적으로? 구현)


@sio.event
async def start_chat(sid, message):
    sio.enter_room(sid, message['question_id'])
    await sio.emit('entered', {'success': True}, room=sid)


@service_api.get('/<question_id>')
@jwt_required
@doc.summary('대화 조회')
async def ChatView(request, token: Token, question_id):
    # user = token.jwt_identity
    # TODO: user['id']를 사용해서 사용자 정보 쿼리 근데 뭐 맞겠지

    # question_id로 question 쿼리
    question = await request.app.db.questions.find_one({
        '_id': ObjectId(question_id)
    })
    if not question:
        abort(404)

    # 상태 확인 -> M이여야 함
    if question['status'] != 'M':
        abort(400)

    # question_id로 chat 쿼리, timestamp로 정렬해 반환
    chats = await request.app.db.chats.find({
        'question_id': question_id
    }).sort('timestamp', pymongo.ASCENDING)

    teachers = await request.app.db.teachers.find({
        'question_id': question_id
    })

    for chat in chats:
        chat['id'] = str(chat['_id'])
        del chat['_id']
        for teacher in teachers:
            if (chat['id'] == teacher['chat_id']):
                del teacher['question_id']
                del teacher['chat_id']
                chat['teacher'] = teacher
        chat['keywords'] = request.app.keywords.search(chat['message'])

    return res_json({'chats': chats})


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

    await sio.emit('update', {}, room=question_id)
    return res_json({})


@service_api.delete('/<question_id>')
@jwt_required
@doc.summary('대화 종료')
async def ChatEnd(request, token: Token, question_id):
    # user = token.jwt_identity

    # question_id의 status를 F로 변경
    res = await request.app.db.questions.update_one({'_id': ObjectId(question_id)}, {
        '$set': {
            'status': 'F'
        }
    })
    if not res.acknowledged:
        abort(500)

    await sio.emit('end', {}, room=question_id)
    return res_json({})


@service_api.post('/request/teacher/<chat_id>')
@jwt_required
@doc.summary('선생님 리뷰 요청')
async def RequestTeacher(request, token: Token, chat_id):
    user = token.jwt_identity

    # chat_id로 question_id 구할 수 있음
    chat = await request.app.db.chats.find_one({
        '_id': ObjectId(chat_id)
    })
    if not chat:
        abort(404)

    question = await request.app.db.questions.find_one({
        '_id': ObjectId(chat['question_id'])
    })
    if not question:
        abort(500, message='question을 찾을 수 없음')

    mentor = await request.app.db.users.find_one({
        '_id': ObjectId(question['user_id'])
    })
    if not mentor:
        abort(500, message='mentor를 찾을 수 없음')

    req = {
        'question_id': question['id'],
        'chat_id': chat['id'],
        'school': mentor['school'],
        'message': request.json['message'],
        'timestamp': int(time.time())
    }
    res = await request.app.db.teachers.insert_one(user)
    if not res.acknowledged:
        abort(500)
    return res_json({})


@service_api.post('/request/offline/<chat_id>')
@jwt_required
@doc.summary('오프라인 멘토링 요청')
async def RequestOffline(request, token: Token, chat_id):
    user = token.jwt_identity

    # chat_id로 question_id 구할 수 있음
    pass
