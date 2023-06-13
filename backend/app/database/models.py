from sqlalchemy import (
    Column,
    VARCHAR,
    DATETIME,
    DATE,
    CHAR,
    PrimaryKeyConstraint,
    UniqueConstraint,
    ForeignKeyConstraint,
    Index,
    Text,
    text
)
from sqlalchemy.dialects.mysql import (
    TINYINT,
    SMALLINT,
    INTEGER,
    BIGINT,
    TINYINT
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()
class Members(Base):
    __tablename__ = "tb_members"

    member_no = Column(SMALLINT(unsigned=True), nullable=False, autoincrement=True, comment="멤버번호")
    member_id = Column(VARCHAR(length=30), nullable=False, comment="사용자 아이디")
    member_pw = Column(VARCHAR(length=128), nullable=False, comment="사용자 패스워드")
    member_name = Column(VARCHAR(length=20), nullable=False, comment="사용자 이름")
    member_email = Column(VARCHAR(length=50), nullable=False, comment="이메일 주소")
    reg_dt = Column(DATETIME(timezone=False), nullable=False, server_default=func.now(), comment="생성일시")
    upd_dt = Column(DATETIME(timezone=False), nullable=False, server_default=func.now(), onupdate=func.now(), comment="수정일시")
    is_deleted = Column(CHAR(length=1), default="F", server_default="F", nullable=False, comment="삭제여부(T|F)")
    del_dt = Column(DATETIME(timezone=False), nullable=True, comment="삭제일시")

    __table_args__ = (
        PrimaryKeyConstraint(member_no, name="pk_members"),
        UniqueConstraint(member_id, name="ixn_members__member_id"),
        {
            "comment": "사용자 정보"
        }
    )

class BoardInfo(Base):
    __tablename__ = 'tb_board_info'

    board_id = Column(VARCHAR(20), nullable=False, comment='게시판아이디')
    board_name = Column(VARCHAR(20), nullable=False, comment='게시판 이름')
    board_type = Column(CHAR(2), nullable=False, comment='게시판타입(L:리스트, G:갤러리)')
    board_auth = Column(CHAR(1), nullable=False, default='M', comment='게시판권한(A: 관리자, M:회원, E:아무나)')
    use_search = Column(CHAR(1), nullable=False, default='T', comment='검색사용여부')
    able_upload = Column(CHAR(1), nullable=False, default='T', comment='파일업로드 가능여부(T|F)')
    reg_dt = Column(DATETIME(timezone=False), nullable=False, server_default=func.now(), comment="생성일시")
    upd_dt = Column(DATETIME(timezone=False), nullable=False, server_default=func.now(), onupdate=func.now(), comment="수정일시")
    is_deleted = Column(CHAR(length=1), default="F", server_default="F", nullable=False, comment="삭제여부(T|F)")
    del_dt = Column(DATETIME(timezone=False), nullable=True, comment="삭제일시")
    __table_args__ = (
        PrimaryKeyConstraint(board_id, name="pk_board_info"),
        {
            "comment": "게시판 정보"
        }
    )

"""
CREATE TABLE `tb_board` (
  `board_no` int unsigned NOT NULL AUTO_INCREMENT COMMENT '게시판번호',
  `board_id` varchar(20) NOT NULL COMMENT '개시판아이디',
  `member_no` int unsigned NULL COMMENT '작성자번호',
  `hit_cnt` mediumint unsigned NOT NULL COMMENT '조회수',
  `title` varchar(255) NOT NULL COMMENT '제목',
  `contents` mediumtext COMMENT '게시글 내용',
  `pure_contents` text COMMENT 'html을 제거한 내용',
  `file_path` varchar(255) DEFAULT NULL COMMENT '첨부파일',
  `ins_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '입력일시',
  `upd_timestamp` timestamp NULL DEFAULT NULL COMMENT '수정일시',
  `is_deleted` char(1) NOT NULL DEFAULT 'F' COMMENT '삭제여부(T|F)',
  `del_timestamp` timestamp NULL DEFAULT NULL COMMENT '삭제일시',
  PRIMARY KEY (`board_no`),
  KEY `ixn_board__board_id` (`board_id`),
  key ixn_board__membrer_no (member_no),
  CONSTRAINT `fk_board__board_id` FOREIGN KEY (`board_id`) REFERENCES `tb_board_info` (`board_id`),
  constraint fk_board__member_no foreign key (member_no) references tb_members (member_no)
);
"""
class Board(Base):
    __tablename__ = 'tb_board'

    board_no = Column(INTEGER(unsigned=True), autoincrement=True, comment='게시판번호')
    board_id = Column(VARCHAR(20), nullable=False, comment='게시판아이디')
    member_no = Column(SMALLINT(unsigned=True), nullable=True, comment='작성자번호')
    hit_cnt = Column(INTEGER(unsigned=True), server_default=0, nullable=False, comment='조회수')
    title = Column(VARCHAR(255), nullable=False, comment='제목')
    contents = Column(Text, comment='게시글 내용')
    pure_contents = Column(Text, comment='html을 제거한 내용')
    reg_dt = Column(DATETIME(timezone=False), nullable=False, server_default=func.now(), comment="생성일시")
    upd_dt = Column(DATETIME(timezone=False), nullable=False, server_default=func.now(), onupdate=func.now(), comment="수정일시")
    is_deleted = Column(CHAR(length=1), default="F", server_default="F", nullable=False, comment="삭제여부(T|F)")
    del_dt = Column(DATETIME(timezone=False), nullable=True, comment="삭제일시")

    __table_args__ = (
        PrimaryKeyConstraint(board_no, name="pk_board"),
        Index("ixn_board__board_id", "board_id"),
        Index("ixn_board__membrer_no", "member_no"),
        ForeignKeyConstraint(
            ["board_id"],
            ["tb_board_info.board_id"],
            name="fk_board__board_id",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        ForeignKeyConstraint(
            ["member_no"],
            ["tb_members.member_no"],
            name="fk_board__member_no",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        {
            "comment": "게시글 리스트"
        }
    )

"""
CREATE TABLE `tb_board_files` (
  `board_files_no` int unsigned NOT NULL AUTO_INCREMENT COMMENT '게시판파일번호',
  `board_no` int unsigned NOT NULL COMMENT '게시판번호',
  `file_mime` varchar(100) NOT NULL COMMENT '파일 MIME',
  `file_path` varchar(255) NOT NULL COMMENT '파일경로',
  `file_name` varchar(100) NOT NULL COMMENT '파일이름',
  `ins_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '입력일시',
  `upd_timestamp` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일시',
  `is_deleted` char(1) NOT NULL DEFAULT 'F' COMMENT '삭제여부(T|F)',
  `del_timestamp` timestamp NULL DEFAULT NULL COMMENT '삭제일시',
  PRIMARY KEY (`board_files_no`),
  KEY `ixn_board_files__board_no` (`board_no`),
  CONSTRAINT `fk_board_files__board_no` FOREIGN KEY (`board_no`) REFERENCES `tb_board` (`board_no`)
);
"""
class BoardFiles(Base):
    __tablename__ = 'tb_board_files'

    board_files_no = Column(INTEGER(unsigned=True), autoincrement=True, comment='게시판파일번호')
    board_no = Column(INTEGER(unsigned=True), nullable=False, comment='게시판번호')
    file_mime = Column(VARCHAR(100), nullable=False, comment='파일 MIME')
    file_path = Column(VARCHAR(255), nullable=False, comment='파일경로')
    file_name = Column(VARCHAR(100), nullable=False, comment='파일이름')
    reg_dt = Column(DATETIME(timezone=False), nullable=False, server_default=func.now(), comment="생성일시")
    upd_dt = Column(DATETIME(timezone=False), nullable=False, server_default=func.now(), onupdate=func.now(), comment="수정일시")
    is_deleted = Column(CHAR(length=1), default="F", server_default="F", nullable=False, comment="삭제여부(T|F)")
    del_dt = Column(DATETIME(timezone=False), nullable=True, comment="삭제일시")

    __table_args__ = (
        PrimaryKeyConstraint(board_files_no, name="pk_board_files"),
        Index("ixn_board_files__board_no", "board_no"),
        ForeignKeyConstraint(
            ["board_no"],
            ["tb_board.board_no"],
            name="fk_board_files__board_no",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        {
            "comment": "게시글 첨부파일 정보"
        }
    )

"""
CREATE TABLE `tb_board_comments` (
	comment_no int unsigned not null auto_increment comment '커멘트번호',
	board_no int unsigned not null comment '게시글번호',
	`member_no` smallint unsigned DEFAULT NULL COMMENT '작성자번호',
	parent_comment_no int unsigned null comment '부모커멘트번호',
	author_name varchar(50) null comment '작성자이름(비로그인)',
	author_pw varchar(32) null comment '비로그인 작성자 인증용',
	contents text not null comment '커멘트 내용',
	reg_dt datetime not null default now() comment '생성일시',
	upd_dt datetime not null default now() on update now() comment '수정일시',
	is_deleted char(1) not null default 'F' comment '삭제여부(T|F)',
	del_dt datetime null comment '삭제일시',
	primary key (comment_no),
	key ixn_board_comments__board_no (board_no),
	key ixn_board_comments__member_no (member_no),
	constraint fk_board_comments__board_no foreign key (board_no) references tb_board (board_no),
    constraint fk_board_comments__member_no foreign key (member_no) references tb_members (member_no)
);
"""
class BoardComments(Base):
    __tablename__ = 'tb_board_comments'

    comment_no = Column(INTEGER(unsigned=True), autoincrement=True, comment='커멘트번호')
    board_no = Column(INTEGER(unsigned=True), nullable=False, comment='게시글번호')
    member_no = Column(SMALLINT(unsigned=True), nullable=True, comment='작성자번호')
    parent_comment_no = Column(INTEGER(unsigned=True), nullable=True, comment='부모커멘트번호')
    author_name = Column(VARCHAR(50), nullable=True, comment='작성자이름(비로그인)')
    author_pw = Column(VARCHAR(32), nullable=True, comment='비로그인 작성자 인증용')
    contents = Column(Text, nullable=False, comment='커멘트 내용')
    reg_dt = Column(DATETIME(timezone=False), nullable=False, server_default=text('now()'), comment='생성일시')
    upd_dt = Column(DATETIME(timezone=False), nullable=False, server_default=text('now()'), onupdate=text('now()'), comment='수정일시')
    is_deleted = Column(CHAR(1), nullable=False, default='F', comment='삭제여부(T|F)')
    del_dt = Column(DATETIME(timezone=False), nullable=True, comment='삭제일시')

    __table_args__ = (
        PrimaryKeyConstraint(comment_no, name="pk_board_comments"),
        Index("ixn_board_comments__board_no", "board_no"),
        Index("ixn_board_comments__member_no", "member_no"),
        ForeignKeyConstraint(
            ["board_no"],
            ["tb_board.board_no"],
            name="fk_board_comments__board_no",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        ForeignKeyConstraint(
            ["member_no"],
            ["tb_members.member_no"],
            name="fk_board_comments__member_no",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        {
            "comment": "게시글 댓글"
        }
    )
