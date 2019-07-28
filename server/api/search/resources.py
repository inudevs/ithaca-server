from server.api.search import search_api
from sanic.response import json as res_json
from sanic_openapi import doc

@search_api.get('/school/<query>')
@doc.summary('학교 자동완성 검색')
@doc.response(200, None, description='성공')
async def SearchSchool(request, query):
    res = request.app.school.autocomplete(query)
    return res_json(res, ensure_ascii=False)
