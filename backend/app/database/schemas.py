from pydantic import BaseModel, Field
from typing import Optional, Literal, List
from datetime import date, datetime

# 회원 가입에 대한 Request Schema
class MemberCreate(BaseModel):
    member_id: str = Field(title="사용자 아이디", max_length=30)
    member_pw: str = Field(title="사용자 패스워드")
    member_name: str = Field(title="사용자 이름", max_length=20)
    member_email: str = Field(title="사용자 이메일", max_length=50)

    class Config:
        orm_mode = True

# 회원 정보 수정에 대한 Request Schema
class MemberModify(BaseModel):
    member_pw: Optional[str] = Field(title="사용자 패스워드")
    member_name: Optional[str] = Field(title="사용자 이름", max_length=20)
    member_email: Optional[str] = Field(title="사용자 이메일", max_length=50)

    class Config:
        orm_mode = True

# JWT Decode에 얻어지는 정보에 대한 Schema
class JWTPayload(BaseModel):
    member_no: int = Field(title="사용자 번호")
    member_id: str = Field(title="사용자 아이디")
    member_name: str = Field(title="사용자 이름")
    member_email: str = Field(title="사용자 이메일")

# 로그인 성공시 Response로 전송되는 Schema
class LoginResponse(BaseModel):
    member_no: int = Field(title="사용자 번호")
    member_id: str = Field(title="사용자 아이디")
    member_name: str = Field(title="사용자 이름")
    member_email: str = Field(title="사용자 이메일")
    access_token: str = Field(title="Access Token")
    refresh_token: str = Field(title="Refresh Token")

class BoardUpsert(BaseModel):
    member_no: Optional[str] = Field(title="작성자 회원 번호")
    title: str = Field(title="게시글 제목")
    contents: str = Field(title="게시글 내용")

class BoardItem(BoardUpsert):
    board_no: int = Field(title="게시물번호")
    board_id: str = Field(title="게시판 아이디")
    hit_cnt: int = Field(title="조회수")
    pure_contents: str = Field(title="태그를 제거한 글 내용")
    reg_dt: datetime = Field(title="생성일시")
    upd_dt: datetime = Field(title="수정일시")

class Message(BaseModel):
    message: str

# Refresh token을 위한 request 정의
class Refresh(BaseModel):
    refresh_token: str = Field(title="Refresh Token")
