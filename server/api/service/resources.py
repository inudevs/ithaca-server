from sanic.exceptions import abort
from sanic.response import json as res_json
from sanic_openapi import doc
from sanic_jwt_extended import jwt_required
from sanic_jwt_extended.tokens import Token
from server import sio
from server.api.service import service_api
from renderer import render_pdf
import pymongo
from bson import ObjectId
from urllib.parse import urljoin
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
    cursor = request.app.db.chats.find({
        'question_id': question_id
    }).sort('timestamp', pymongo.ASCENDING)
    chats = await cursor.to_list(length=50)

    cursor = request.app.db.teachers.find({
        'question_id': question_id
    })
    teachers = await cursor.to_list(length=50)

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


@service_api.post('/feedback/<question_id>')
@jwt_required
@doc.summary('대화 피드백')
async def ChatFeedback(request, token: Token, question_id):
    user = token.jwt_identity
    question = await request.app.db.questions.find_one({
        '_id': ObjectId(question_id)
    })
    if not question:
        abort(500, message='question을 찾을 수 없음')
    if question['user_id'] == user['id']:
        # user is mentee
        sender = 'mentee'
    else:
        sender = 'mentor'

    feedback = {
        'question_id': question_id,
        'sender': sender,
        'user_id': user['id'],
        'message': request.json['message'],
        'timestamp': int(time.time())
    }
    res = await request.app.db.feedbacks.insert_one(feedback)
    if not res.acknowledged:
        abort(500)
    return res_json({'id': str(res.inserted_id)})


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
    res = await request.app.db.teachers.insert_one(req)
    if not res.acknowledged:
        abort(500)
    return res_json({})


@service_api.post('/request/offline/<chat_id>')
@jwt_required
@doc.summary('오프라인 멘토링 요청')
# model: { time, place, message }
async def RequestOffline(request, token: Token, chat_id):
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
    if question['user_id'] == user['id']:
        # user is mentee
        sender = 'mentee'
    else:
        sender = 'mentor'

    # user_id로 sender 구하고, text 타입의 chat 만들어 저장
    chat = {
        'type': 'offline',
        'question_id': question['id'],
        'sender': sender,
        'message': request.json['message'],
        'timestamp': int(time.time()),
        'offline': {
            'time': request.json['time'],
            'place': request.json['place']
        }
    }
    res = await request.app.db.chats.insert_one(chat)
    if not res.acknowledged:
        abort(500)

    await sio.emit('update', {}, room=question['id'])
    return res_json({})


@service_api.get('/pdf/<question_id>')
@doc.summary('Render PDF file of mentoring')
async def RenderPDF(request, question_id):
    # 1. query question
    question = await request.app.db.questions.find_one({
        '_id': ObjectId(question_id)
    })
    if not question:
        abort(500, message='question을 찾을 수 없음')

    # 2. assert question status == C
    if question['status'] != 'C':
        abort(400, message='아직 끝나지 않은 멘토링')

    # 3. assert question has null in portfolio field
        # return value as url if value
    if question['portfolio']:
        return res_json({
            'url': question['portfolio']
        })

    # 4. get post, mentor from question
    mentor = await request.app.db.users.find_one({
        '_id': ObjectId(question['user_id'])
    })
    if not mentor:
        abort(500, message='mentor를 찾을 수 없음')

    # 5. query requests to get mentee
    req = await request.app.db.requests.find_one({
        'question_id': question_id,
        'approved': True
    })
    if not req:
        abort(500, message='request를 찾을 수 없음')

    mentee = await request.app.db.users.find_one({
        '_id': ObjectId(req['user_id'])
    })
    if not mentee:
        abort(500, message='mentee를 찾을 수 없음')

    # 6. query chats
    cursor = request.app.db.chats.find({
        'question_id': question_id
    }).sort('timestamp', pymongo.ASCENDING)
    chats = await cursor.to_list(length=50)

    # 7. query feedbacks
    mentor_feedback = await request.app.db.feedbacks.find_one({
        'question_id': question_id,
        'sender': 'mentor'
    })
    mentee_feedback = await request.app.db.feedbacks.find_one({
        'question_id': question_id,
        'sender': 'mentee'
    })

    pdf_data = {
        'subject': question['cartegory'],
        'start_date': '',
        'end_date': '',
        'mentor': mentor['name'],
        'mentee': mentee['name'],
        'question': {
            'category': question['category'],
            'time': question['timestamp'],
            'title': question['title'],
            'article': question['article'],
            'photo': question['photo'],
        },
        'chats': chats,
        'feedbacks': {
            'mentor': mentor_feedback,
            'mentee': mentee_feedback
        }
    }

    # 8. render pdf
    file_path = render_pdf(pdf_data, question_id)
    pdf_url = urljoin(request.app.config['BASE_URL'], file_path)
    res = await request.app.db.questions.update_one({'_id': ObjectId(question_id)}, {
        '$set': {
            'portfolio': pdf_url
        }
    })
    if not res.acknowledged:
        abort(500)
    return res_json({
        'url': pdf_url
    })
