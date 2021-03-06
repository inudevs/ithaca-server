from sanic import Sanic, Blueprint
from sanic.response import json as res_json
from sanic_openapi import swagger_blueprint, doc
from sanic_cors import CORS
from sanic_jwt_extended import JWTManager
from motor.motor_asyncio import AsyncIOMotorClient
import socketio
from config import DevConfig
import school
import keywords


sio = socketio.AsyncServer(async_mode='sanic')


def create_app():
    _app = Sanic(__name__)
    _app.config.from_object(DevConfig)
    JWTManager(_app)
    CORS(_app)

    _app.blueprint(swagger_blueprint)

    @_app.listener('before_server_start')
    def init(app, loop):
        _app.db = AsyncIOMotorClient(_app.config.MONGO_URI)[
            _app.config.MONGO_DB]

    from server.api import api
    _app.blueprint(api)
    _app.static('/uploads', './uploads')
    _app.school = school
    _app.keywords = keywords

    return _app


app = create_app()


@app.get('/')
async def index(request):
    return res_json({
        'message': 'Welcome to Ithaca API Server',
        'docs': '/swagger',
        'github': 'https://github.com/inudevs/ithaca-server'
    }, escape_forward_slashes=False)
