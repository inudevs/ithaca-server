from sanic.exceptions import abort
from sanic.response import json as res_json
from sanic_openapi import doc
from server.api.upload import upload_api
from server.api.upload.models import ResponseModel
import mathpix
import os
import time
from urllib.parse import urljoin
from functools import reduce


@upload_api.post('/profile')
@doc.summary('프로필 사진 업로드')
@doc.produces(ResponseModel, content_type='application/json', description='성공')
@doc.response(200, None, description='성공')
@doc.response(500, None, description='에러')
async def UploadProfile(request):
    profile_image = request.files.get('file')
    _, ext = os.path.splitext(profile_image.name)
    timestamp = int(time.time())
    file_path = './profile/{}'.format(str(timestamp) + ext)

    with open(os.path.join('.{}'.format(request.app.config['UPLOAD_PATH']), file_path), 'wb') as fp:
        fp.write(profile_image.body)
    return res_json({
        'url': urljoin(request.app.config['UPLOAD_PATH'], file_path)
    }, escape_forward_slashes=False)


@upload_api.post('/prob')
@doc.summary('문제 사진 업로드')
async def UploadProb(request):
    profile_image = request.files.get('file')
    _, ext = os.path.splitext(profile_image.name)
    timestamp = int(time.time())
    file_path = './prob/{}'.format(str(timestamp) + ext)

    with open(os.path.join('.{}'.format(request.app.config['UPLOAD_PATH']), file_path), 'wb') as fp:
        fp.write(profile_image.body)
    image_url = reduce(urljoin, [
        request.app.config['BASE_URL'],
        request.app.config['UPLOAD_PATH'],
        file_path
    ])
    return res_json({
        'url': image_url,
        'category': '수학' # example output
    }, escape_forward_slashes=False)


@upload_api.post('/math')
@doc.summary('수식 업로드')
async def UploadMath(request):
    profile_image = request.files.get('file')
    _, ext = os.path.splitext(profile_image.name)
    timestamp = int(time.time())
    file_path = './math/{}'.format(str(timestamp) + ext)

    with open(os.path.join('.{}'.format(request.app.config['UPLOAD_PATH']), file_path), 'wb') as fp:
        fp.write(profile_image.body)
    image_url = reduce(urljoin, [
        request.app.config['BASE_URL'],
        request.app.config['UPLOAD_PATH'],
        file_path
    ])
    return res_json({
        'url': image_url,
        'math': mathpix.api.image_to_math(image_url)
    }, escape_forward_slashes=False)
