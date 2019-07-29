from sanic import Blueprint

service_api = Blueprint(
    'service',
    url_prefix='/service',
    strict_slashes=True
)

__import__('server.api.service.resources')
