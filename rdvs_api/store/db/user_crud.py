"""
Name:    crud
Author:  ReddyFan
Date:    2023/1/14 17:17
Desc:  
"""
from sqlalchemy.orm import Session

import models
from schemas.user import UserCreate
from utils.user_verification import get_password_hash


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def query_user(db: Session, user_id: int):
    return db.query(models.User).filter_by(user_id=user_id).with_entities(
        models.User.profile,
        models.User.username,
        models.User.desc,
        models.User.gender,
        models.User.birth,
        models.User.tel,
        models.User.email,
        models.User.vocation,
        models.User.area
    ).first()


def query_username(db: Session, username: str):
    return db.query(models.User).filter_by(username=username).count()


def query_tel(db: Session, tel: str):
    return db.query(models.User).filter_by(tel=tel).count()


def query_email(db: Session, email: str):
    return db.query(models.User).filter_by(email=email).count()


# def get_user2(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    db_user = models.User(**user.dict())
    db_user.password = get_password_hash(user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return user


def update_simple_info(db: Session, user_id: int, key: str, value: str):
     user = db.query(models.User).filter(models.User.user_id == user_id).first()
     if user:
         user.__setattr__(key, value)
         db.commit()
         return  True
     return  False
