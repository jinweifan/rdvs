"""
Name:    user
Author:  ReddyFan
Date:    2023/3/23 15:10
Desc:  处理用户逻辑
"""
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Body
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm import Session
from starlette import status

from dependencies import get_db
from models import User
from schemas.user import UserCreate
from store.db import user_crud
from store.db.user_crud import query_user, query_username, query_tel, query_email, update_simple_info
from utils.user_verification import CUMPasswordRequestForm, create_access_token, \
    ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, get_current_active_user

router = APIRouter()


# @router.post("/token")
# async def get_token(token: str = Depends(oauth2_scheme)):
#     return {"token": token}

# usernameIsExist

@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    tags=["users"],
)
async def user_is_exist(username: str = Query(None), tel: str = Query(None), email: str = Query(None),
                        db: Session = Depends(get_db)):
    if username:
        flag = query_username(db, username)
    elif tel:
        flag = query_tel(db, tel)
    else:
        flag = query_email(db, email)
    return {'data': {'flag': flag}}


@router.post(
    "/register",
    # response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["users"],
    operation_id="some_specific_id_you_define"
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        resp_user = user_crud.create_user(db=db, user=user)
    except IntegrityError as e:
        if e.orig.args[0] == 1062:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已存在")
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="数据库异常")
    except DataError as e:
        raise HTTPException(status_code=404, detail="数据库出错")
    return resp_user


@router.post("/login")
async def login(form_data: CUMPasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print('form: ', form_data.__dict__)
    user = authenticate_user(db, form_data.username, form_data.password)
    print('user: ', user)
    if not user:
        raise HTTPException(status_code=401, detail="用户或密码错误！")
    elif user.is_locked:
        raise HTTPException(status_code=401, detail="账号已被冻结！")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"user_id": user.user_id, "username": user.username, "access_token": access_token, "token_type": "bearer",
            "detail": "登录成功！"}


@router.get("/me")
async def me(user: User = Depends(get_current_active_user)):
    return user


@router.get(
    '/{user_id}',
    status_code=status.HTTP_200_OK,
    tags=["users"],
)
async def get_user(user_id: int = Path(...), db: Session = Depends(get_db)):
    """
    获取用户
    :param user_id: 用户ID
    :param db: 数据库会话
    :return:
    """
    user = query_user(db, user_id)
    print('user:{}'.format(user))
    return {'data': {'user': user}}


@router.patch(
    '/{user_id}',
    status_code=status.HTTP_200_OK,
    tags=["users"])
async def update_user_info(user_id: int = Path(...), key: str = Body(...), value: str = Body(...),
                           db: Session = Depends(get_db)):
    flag = update_simple_info(db, user_id, key, value)
    print('update_user_info flag', flag)
    if flag:
        return {"code": 1001}
    else:
        return {"code": 2001}
