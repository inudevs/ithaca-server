from sanic import Blueprint
from server.api.auth import auth_api
from server.api.upload import upload_api
from server.api.search import search_api
from server.api.question import question_api
from server.api.mentor import mentor_api
from server.api.service import service_api

api = Blueprint.group(
    auth_api,
    upload_api,
    search_api,
    question_api,
    mentor_api,
    service_api
)
