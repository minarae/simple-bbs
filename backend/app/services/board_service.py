from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from typing import Optional
from ..database import models, schemas
from ..libraries.util import remove_html_tags

# 게시판 속성 가져오기
async def get_board_info(
    db: AsyncSession,
    board_id: str,
):
    stmt = select(models.BoardInfo).filter(
        models.BoardInfo.board_id == board_id,
        models.BoardInfo.is_deleted == 'F'
    )

    result = await db.execute(stmt)
    return result.fetchone()

# 게시판 게시글 리스트
async def board_list(
    db: AsyncSession,
    board_id: str,
    search: dict,
    is_cnt: bool,
):
    stmt = select(models.Board)
    # 조회된 전체 리스트 수를 가져오는 경우
    if is_cnt:
        stmt = select(func.count(models.Board.board_no))

    # 조건(page, offest, 검색조건 등)에 맞는 게시글 리스트 조회
    stmt = stmt.filter(
        models.Board.board_id == board_id,
        models.Board.is_deleted == 'F'
    )

    # 검색된 수를 찾는 경우는 조회 조건까지만 적용하고 반환
    if is_cnt:
        result = await db.execute(stmt)
        return result.scalar()

    # 리스트를 가져오는 경우는 offset, orderby 적용
    if search['page'] is not None and search['offset'] is not None:
        stmt = stmt.offset((search['page'] - 1) * search['offset']).limit(search['offset'])

    # Specify the field for ORDER BY
    order_by_field = 'board_no'
    if search['order'] is not None:
        order_by_field = search['order']

    # Specify the sort order
    sort_order = 'desc'  # 'asc' for ascending order
    if search['sort_order'] is not None:
        sort_order = search['sort_order']

    # Execute a query with dynamic ORDER BY and sort order
    column_attr = getattr(models.Board.__table__.c, order_by_field)
    if sort_order == 'desc':
        column_attr = column_attr.desc()

    stmt = stmt.order_by(column_attr)
    result = await db.execute(stmt)

    return result.fetchall()

# 게시글 생성
async def create_post(
    db: AsyncSession,
    board_id: str,
    post: schemas.BoardUpsert,
):
    # 여기로 진입하기 전에 권한 체크를 먼저 해야함.
    post_dict = post.dict()
    pure_text = remove_html_tags(post_dict["contents"])
    db_post = models.Board(**post_dict, pure_contents=pure_text, board_id=board_id)
    db.add(db_post)

    # 파일이 있으면 파일 업로드도 처리해야 해야함
    await db.commit()
    await db.refresh(db_post)

    return db_post

# 게시글 조회
async def get_post(
    db: AsyncSession,
    board_no: int,
):
    # 게시물이 존재하는지 확인
    result = await db.execute(
        select(models.Board).filter(
            models.Board.board_no == board_no,
            models.Board.is_deleted == 'F',
        )
    )
    db_post = result.scalars().first()

    # 첨부된 댓글 리스트 조회

    # 첨부 파일 리스트 조회

    return db_post

# 게시글 수정

# 게시글 삭제
async def delete_post(
    db: AsyncSession,
    member_no: Optional[int],
    board_no: int,
):
    # 게시물이 존재하는지 확인
    result = await db.execute(
        select(models.Board).filter(
            models.Board.board_no == board_no,
            models.Board.is_deleted == 'F',
        )
    )
    db_post = result.scalars().first()

    if db_post is None:
        raise Exception("게시물 정보를 찾을 수 없습니다.")

    if db_post.member_no is not None and db_post.member_no != member_no:
        raise Exception('게시물 수정에 대한 권한이 없습니다')

    setattr(db_post, 'is_deleted', 'T')
    setattr(db_post, 'del_dt', func.now())

    await db.commit()
    return db_post

# 댓글 생성

# 댓글 수정

# 댓글 삭제
