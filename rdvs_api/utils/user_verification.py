"""
@Time ： 2021/5/29 16:59
@Auth ： Melon
@File ：user_verification.py
@Description : 工具
"""
import hashlib
import random
import re
import string
from datetime import timedelta, datetime
from typing import Optional, Union

from fastapi import requests, Form, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from dependencies import get_db
from models import User
from schemas.token import TokenData

# 所有字符
ALL_CHARS = string.ascii_letters + string.digits
# 数字
ALL_NUMS = string.digits
# 账户验证正则
ACCOUNT_PATTERN = re.compile(
    r'\w{6,20}|^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z\d_-]+(\.[a-zA-Z\d_-]+)+$')
# 手机号验证正则
TEL_PATTERN = re.compile(r'1[3-9]\w{9}')
# 密码验证码正则
PASSWORD_PATTERN = re.compile(r'[\da-zA-Z]{6,30}')
# 图片验证码正则
CAPTCHA_PATTERN = re.compile(r'[\da-zA-Z]{4}')

# # 创建随机token秘钥  openssl rand -hex 32
# SECRET_KEY = "75cf3048b0a7214476657f07238c2569142718ed806fc571e1c30e52e5f3e4eb"
# # token使用的算法
# ALGORITHM = "HS256"
# # token过期时间
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

SECRET_KEY = "b342662c541cba035b904055e0be4f86a17cdce2dfd2967eed3807f4ff5f87ad"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# oauth2验证
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")
# Passlib 是处理密码哈希的 Python 包，推荐的算法是 Bcrypt。
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """ 验证哈希密码 """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """ 获取hash密码 """
    return pwd_context.hash(password)


def authenticate_user(db, username: str, password: str):
    """ 授权用户 """
    from store.db.user_crud import get_user
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """
    创建token
    :param data:
    :param expires_delta:
    :return:
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    通过token获取当前用户信息
    :param db:
    :param token:
    :return:
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print('token', token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    from store.db.user_crud import query_user
    user = query_user(db, username=token_data.username)
    print(user.__dict__)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    用户冻结状态验证
    :param current_user:
    :return: 用户对象
    """
    print('current_user.is_locked', current_user.is_locked)
    if current_user.is_locked:
        raise HTTPException(status_code=400, detail="该账号处于冻结状态")
    return current_user


def send_message_by_sms(*, tel, message):
    """
    调用腾讯短信接口
    :param tel:
    :param message:
    :return: 返回json数据
    """
    resp = requests.post(
        url='http://sms-api.luosimao.com/v1/send.json',
        auth=('api', 'key-a191efa9e007373daf2c838a98533405'),
        data={
            'mobile': tel,
            'message': message
        }, timeout=3, verify=False)
    return resp.json()


def random_picture_code(length=4):
    """
    生成图片验证码
    :param length:
    :return:
    """
    return ''.join(random.choices(ALL_CHARS, k=length))


def random_mobile_code(length=6):
    """
    生成手机号验证码
    :param length:
    :return:
    """
    return ''.join(random.choices(ALL_NUMS, k=length))


def check_captcha(captcha):
    """ 检查验证码 """
    return CAPTCHA_PATTERN.fullmatch(captcha) is not None


def check_account(account):
    """ 检查账号 """
    return ACCOUNT_PATTERN.fullmatch(account) is not None


def check_password(password):
    """ 检查密码 """
    return PASSWORD_PATTERN.fullmatch(password) is not None


def check_tel(tel):
    """ 检查手机号 """
    return TEL_PATTERN.fullmatch(tel) is not None


def gen_md5_digest(content):
    """将字符串处理成MD5摘要"""
    return hashlib.md5(content.encode()).hexdigest()


def gen_sha256_digest(content):
    """将字符串处理成SHA-256摘要"""
    return hashlib.sha256(content.encode()).hexdigest()


class CUMPasswordRequestForm(OAuth2PasswordRequestForm):
    """ 自定义认证表单 """

    def __init__(
            self,
            verification_code: str = Form(
                default=None, regex=r'[0-9a-zA-Z]{4}'),
            grant_type: str = Form(default=None, regex="password"),
            username: str = Form(),
            password: str = Form(),
            scope: str = Form(default=""),
            client_id: Optional[str] = Form(default=None),
            client_secret: Optional[str] = Form(default=None),
    ):
        self.verification_code = verification_code
        super().__init__(
            grant_type,
            username,
            password,
            scope,
            client_id,
            client_secret,
        )


if __name__ == '__main__':
    pwd = input("请输入密码：")
    hash_pwd = get_password_hash(pwd)
    flag = verify_password(pwd, hash_pwd)
    print('原密码是否相等：{:^10}'.format(flag))
