# Ithaca API Server

## To-Do List

- **인증** (auth)
    - [x] 회원가입
        - [x] 학교 검색 자동완성 (search/)
        - [x] 프로필 사진 업로드 (upload/)
    - [x] 로그인
- **질문** (question)
    - [x] 질문 목록 + 필터링
    - [x] 질문 게시
        - [x] 문제 사진 업로드 -> 카테고리 (upload/)
    - [x] 질문 조회
- **멘토링 매칭** (mentor)
    - [x] 멘토링 신청
    - [x] 멘토링 승인
    - [x] 멘토링 목록
- **멘토링 대화** (service)
    - [x] 대화 조회
    - [x] 대화 전송
        - 대화 중 추가 서비스
            - [x] 수식 업로드 (upload/)
            - [x] 선생님 리뷰 요청
            - [x] 오프라인 멘토링 요청
    - [x] 대화 종료
    - [x] 피드백 전송
    - [x] 포트폴리오 출력
- **선생님 API** (teacher)
    - [ ] 선생님 가입
    - [ ] 선생님 로그인
    - [ ] 리뷰 요청 목록
    - [ ] 리뷰 요청 답변

## Run
Simple method:
```
sudo nohup /home/ubuntu/.local/bin/uvicorn server:app --host 0.0.0.0 --port 80
```

or use [nginx](https://www.nginx.com) or something

## Config
```python
MONGO_URI = 'mongodb://example.com:59077' # mongoDB URI without DB name
MONGO_DB = 'ithaca' # DB name
BASE_URL = 'http://example.com/' # Base URL
```
