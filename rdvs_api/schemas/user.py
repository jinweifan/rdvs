"""
Name:    user
Author:  ReddyFan
Date:    2023/1/15 09:05
Desc:  
"""
from datetime import datetime
from typing import Union

from fastapi import Form
from pydantic import BaseModel
from pymysql import Date

from utils.DateTime import DATE_FORMAT


class UserBase(BaseModel):
    username: str = Form(..., unique=True, min_length=2, max_length=10)


SEX_OPTIONS = ((True, '男'), (False, '女'))
TEL_REGEX: str = r'1[3-9]\d{9}'
PASSWORD_REGEX: str = r'[0-9a-zA-Z]{6,30}'
VERIFICATION_CODE_REGEX: str = r'[0-9a-zA-Z]{4}'
EMAIL_REGEX: str = r'^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$'


class User(BaseModel):
    profile: str
    tel: str
    gender: bool
    is_locked: bool = True


class UserCreate(UserBase):
    """ 新增用户模型 """
    password: str = Form(..., min_length=6, max_length=64)
    tel: Union[str, None] = Form(..., unique=True, min_length=11, max_length=11, regex=TEL_REGEX)
    email: Union[str, None] = Form(..., unique=True, min_length=8, max_length=30, regex=EMAIL_REGEX)
    gender: bool = Form(default=True)
    # birth: Date = Form(...)
    # area: str = Form(default=None)


class UserResponse(UserBase):
    """ 新增用户响应模型 """
    profile: str = Form(default=None, max_length=200)
    tel: Union[str, None] = Form(..., regex=TEL_REGEX)
    email: Union[str, None] = Form(..., min_length=8, max_length=30)
    gender: bool = Form(default=True)
    birth: Date = Form(...)
    area: str = Form(default=None)
    reg_time: datetime = Form(default=datetime.now().strftime(DATE_FORMAT))
    last_login: Union[datetime, None] = Form(default=datetime.now().strftime(DATE_FORMAT))
    desc: str = Form(default=None, min_length=10, max_length=200)
    vocation: str = Form(default=None, min_length=2)
    is_locked: bool = Form(default=False)
    is_deleted: bool = Form(default=False)

    class Config:
        orm_mode = True


class LoginUser(UserBase):
    """ 登录模型 """
    password: str = Form(..., regex=PASSWORD_REGEX)
    verification_code: str = Form(..., regex=VERIFICATION_CODE_REGEX)
