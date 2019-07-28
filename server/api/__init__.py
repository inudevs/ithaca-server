from sanic import Blueprint
from server.api.auth import auth_api
from server.api.upload import upload_api

api = Blueprint.group(
    auth_api,
    upload_api
)
