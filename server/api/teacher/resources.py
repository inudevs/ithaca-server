from sanic.exceptions import abort
from sanic.response import json as res_json
from sanic_openapi import doc
from sanic_jwt_extended import jwt_required
from sanic_jwt_extended.tokens import Token
from server.api.teacher import teacher_api
import os
import time


@teacher_api.post('/join')
@doc.summary('선생님 회원가입')
async def TeacherJoin(request):
    pass

@teacher_api.post('/login')
@doc.summary('선생님 로그인')
async def TeacherLogin(request):
    pass

@teacher_api.get('/dashboard')
@jwt_required
@doc.summary('선생님 대시보드')
async def TeacherDashboard(request, token: Token):
    pass

@teacher_api.post('/answer/<request_id>')
@jwt_required
@doc.summary('선생님 리뷰 응답')
async def TeacherAnswer(request, token: Token, request_id):
    pass
