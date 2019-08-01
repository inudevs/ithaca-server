from sanic import Blueprint

teacher_api = Blueprint(
    'teacher',
    url_prefix='/teacher',
    strict_slashes=True
)

__import__('server.api.teacher.resources')
