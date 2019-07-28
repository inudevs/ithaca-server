from sanic_openapi import doc


class LoginModel:
    email = doc.String('이메일', required=True)
    password = doc.String('패스워드', required=True)


class UserModel:
    id = doc.Integer('사용자 오브젝트 id')
    name = doc.String('이름')
    school = doc.String('학교')
    grade = doc.Integer('학년')
    klass = doc.Integer('반')
    number = doc.Integer('번호')
    photo = doc.String('프로필 사진')  # URL for profile
    user_type = doc.String('회원 종류')  # S / T
    email = doc.String('이메일')
    password = doc.String('패스워드')


class TokenModel:
    token = doc.String('JWT 토큰')
    refresh_token = doc.String()
    user = UserModel
