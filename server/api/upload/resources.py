from sanic.exceptions import abort
from sanic.response import json as res_json
from sanic_openapi import doc
from server.api.upload import upload_api
import os
import time
import urllib.parse


@upload_api.post('/profile')
@doc.summary('프로필 사진 업로드')
@doc.response(200, None, description='성공')
@doc.response(500, None, description='에러')
async def UploadProfile(request):
    profile_image = request.files.get('file')
    _, ext = os.path.splitext(profile_image.name)
    timestamp = int(time.time())
    file_path = './profile/{}'.format(str(timestamp) + ext)

    with open(os.path.join(request.app.config['UPLOAD_DIR'], file_path), 'wb') as fp:
        fp.write(profile_image.body)
    return res_json({
        'url': urllib.parse.urljoin('/uploads/', file_path)
    }, escape_forward_slashes=False)