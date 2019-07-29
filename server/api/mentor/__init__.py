from sanic import Blueprint

mentor_api = Blueprint(
    'mentor',
    url_prefix='/mentor',
    strict_slashes=True
)

__import__('server.api.mentor.resources')
