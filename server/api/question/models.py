from sanic_openapi import doc
from server.api.mentor.models import RequestModel

class QuestionModel:
    id = doc.String('질문 오브젝트 id')
    user_id = doc.Integer('작성자 오브젝트 id')
    title = doc.String('제목')
    article = doc.String('본문')
    cartegory = doc.String('카테고리')
    photo = doc.String('문제 사진')  # URL for photo
    requests = doc.List(RequestModel)
    status = doc.String() # P for pending
    portfolio = doc.String() # URL for portfolio

class CreateQuestionModel:
    title = doc.String('제목')
    article = doc.String('본문')
    cartegory = doc.String('카테고리')
    photo = doc.String('문제 사진')  # URL for photo
