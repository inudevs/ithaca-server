from sanic import Blueprint
from sanic.response import json as res_json
# from server.api.auth import auth_api

test = Blueprint('test', url_prefix='/')

@test.route('/')
async def bp1_route(request):
    return res_json({ 'test': True })

api = Blueprint.group(
    test,
    # auth_api
)
