from sanic import Sanic, Blueprint
from sanic_openapi import swagger_blueprint, doc
from sanic_cors import CORS
from sanic_jwt_extended import JWTManager
from motor.motor_asyncio import AsyncIOMotorClient
from config import DevConfig
from server.api import api
import school


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

    _app.blueprint(api)
    _app.static('/uploads', './uploads')
    _app.school = school

    return _app


app = create_app()
