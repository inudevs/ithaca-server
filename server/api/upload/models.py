from sanic_openapi import doc


class ResponseModel:
    url = doc.String('업로드된 파일 URL', required=True)
