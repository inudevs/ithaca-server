from sanic import Blueprint

question_api = Blueprint(
    'question',
    url_prefix='/question',
    strict_slashes=True
)

__import__('server.api.question.resources')
