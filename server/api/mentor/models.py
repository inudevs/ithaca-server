from sanic_openapi import doc


class RequestModel:
    id = doc.String()
    user_id = doc.String()
    question_id = doc.String()
    timestamp = doc.Integer()
