from sanic.exceptions import abort
from sanic.response import json as res_json
from sanic_openapi import doc
from sanic_jwt_extended import create_access_token, create_refresh_token
from server.api.auth import auth_api
from server.api.auth.models import LoginModel, TokenModel, UserModel


@auth_api.post('/join')
@doc.summary('회원가입')
@doc.consumes(UserModel, content_type='application/json', location='body')
@doc.response(200, None, description='성공')
@doc.response(400, None, description='잘못된 요청')
@doc.response(500, None, description='에러')
async def AuthJoin(request):
    try:
        keys = [
            'name',
            'school',
            'grade',
            'klass',
            'number',
            'photo',
            'user_type',
            'email',
            'password']
        user = {}
        for key in keys:
            user[key] = request.json[key]
    except BaseException:
        return res_json(400)
    if await request.app.db.users.find_one({
        'email': user['email']
    }):
        abort(400)
    res = await request.app.db.users.insert_one(user)
    if not res.acknowledged:
        abort(500)
    return res_json({})


@auth_api.post('/login')
@doc.summary('로그인')
@doc.consumes(LoginModel, content_type='application/json', location='body')
@doc.produces(TokenModel, content_type='application/json', description='성공')
@doc.response(404, None, description='잘못된 로그인 정보')
async def AuthLogin(request):
    email, password = request.json['email'], request.json['password']

    user = await request.app.db.users.find_one({
        'email': email,
        'password': password
    })
    if not user:
        abort(404)

    user['id'] = str(user['_id'])
    for key in ['_id', 'password']:
        del user[key]

    identity = {
        'id': user['id'],
        'name': user['name']
    }
    token = await create_access_token(identity=identity, app=request.app)
    refresh_token = await create_refresh_token(identity=identity, app=request.app)
    return res_json({
        'token': token,
        'refresh_token': refresh_token,
        'user': user
    })
