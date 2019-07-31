from sanic_openapi import doc


class ChatModel:
    id = doc.String('대화 오브젝트 id')
    type = doc.String()  # image, text
    question_id = doc.String()
    sender = doc.String()  # mentor, mentee
    message = doc.String()
    timestamp = doc.Integer()
