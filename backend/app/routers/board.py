from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from starlette.responses import Response, JSONResponse
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from ..database.connection import get_db
from ..database import schemas
from ..services import members_service
from ..libraries import auth

router = APIRouter(
    prefix="/board",
    tags=["board"],
    responses={
        404: {"description": "Not Found"},
    }
)

# 게시글 리스트
@router.put("/{board_name}", description="게시글 리스트", response_class=Response, responses={
    HTTP_400_BAD_REQUEST: {
        "model": schemas.Message
    }
})
async def board_list(
    db: AsyncSession = Depends(get_db)
):
    # 게시판 성속 가져오기
    pass

# 게시글 작성 처리

# 게시글 읽기

# 게시글 수정

# 게시글 삭제

# 댓글 달기

# 댓글 수정

# 댓글 삭제
