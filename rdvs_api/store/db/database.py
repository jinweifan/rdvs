"""
Name:    database.py
Author:  ReddyFan
Date:    2023/1/14 17:18
Desc:  
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:melon2021@1.116.250.241:3306/rdvs?charset=utf8"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # encoding="utf-8",
    echo=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

if __name__ == '__main__':
    #
    # from sqlalchemy.orm import sessionmaker
    # from sqlalchemy import create_engine
    #
    # engine = create_engine(SQLALCHEMY_DATABASE_URL)
    # Session = sessionmaker(bind=engine)
    # session = Session()
    #
    # user = session.query(User).filter_by(user_id=1).first()
    # print(user)
    pass
