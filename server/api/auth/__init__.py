from sanic import Blueprint
from sanic.exceptions import abort
from sanic.response import json as res_json
from sanic_openapi import doc
from sanic_jwt_extended import create_access_token, create_refresh_token
from server.api.auth.models import LoginModel, TokenModel

auth_api = Blueprint(
    'auth',
    url_prefix='/auth',
    strict_slashes=True
)

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
    identity = {
        'id': str(user['_id']),
        'name': user['name']
    }
    token = await create_access_token(identity=identity, app=request.app)
    refresh_token = await create_refresh_token(identity=identity, app=request.app)
    return res_json({
        'token': token,
        'refresh_token': refresh_token,
        'user': user
    })
