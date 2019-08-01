from sanic_openapi import doc


class ChatModel:
    id = doc.String('대화 오브젝트 id')
    type = doc.String()  # image, text
    question_id = doc.String()
    sender = doc.String()  # mentor, mentee
    message = doc.String()
    timestamp = doc.Integer()


class TeacherRequestModel:
    id = doc.String('선생님 리뷰 요청 오브젝트 id')
    question_id = doc.String()
    chat_id = doc.String()
    school = doc.String('학교 이름')
    message = doc.String('메세지')
    timestamp = doc.Integer()
