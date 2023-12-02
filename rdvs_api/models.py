"""
Name:    models.py
Author:  ReddyFan
Date:    2023/1/25 17:02
Desc:  
"""

from datetime import datetime

from sqlalchemy import Boolean, Column, BigInteger, VARCHAR, Date, DateTime

from store.db.database import Base


class BaseModel(Base):
    __abstract__ = True

    # id = Column(BigInteger, primary_key=True, autoincrement=True)
    is_deleted = Column(Boolean, default=False)
    deleted_time = Column(DateTime, default=None)


class User(BaseModel):
    """ 用户模块 """
    __tablename__ = "tb_user"

    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    profile = Column(VARCHAR(200))
    username = Column(VARCHAR(20))
    password = Column(VARCHAR(20))
    tel = Column(VARCHAR(11), unique=True, nullable=False)
    email = Column(VARCHAR(30), unique=True, nullable=False)
    gender = Column(Boolean, default=True, )
    birth = Column(Date, default=datetime.date(datetime.now()))
    area = Column(VARCHAR(50))
    create_time = Column(DateTime, default=datetime.now)
    last_login = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    vocation = Column(VARCHAR(20), nullable=False)
    is_locked = Column(Boolean, default=False)

    # work_diary = relationship("WorkDiary", back_populates="user")

# class WorkDiary(BaseModel):
#     __tablename__ = "tb_work_diary"
#
#     user_id = Column(BigInteger, ForeignKey("tb_user.id"))
#     # category_id = ForeignKey()
#     title = Column(VARCHAR(20), unique=True)
#     content = Column(TEXT())
#     # template = Column(VARCHAR(20))
#     create_time = Column(DateTime, default=datetime.now)
#     pub_time = Column(DateTime, default=None)
#     update_time = Column(DateTime, default=datetime.now)
#
#     user = relationship("User", back_populates="work_diary")
