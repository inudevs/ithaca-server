from sanic import Blueprint

search_api = Blueprint(
    'search',
    url_prefix='/search',
    strict_slashes=True
)

__import__('server.api.search.resources')
