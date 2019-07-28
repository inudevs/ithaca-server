from sanic import Blueprint

upload_api = Blueprint(
    'upload',
    url_prefix='/upload',
    strict_slashes=True
)

__import__('server.api.upload.resources')
