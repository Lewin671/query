# coding: utf-8
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URI

# 表格对象需要继承的基类
Base = declarative_base()


# 创建一个engine
def create_engine():
    engine = sqlalchemy.create_engine('sqlite:///' + DATABASE_URI,connect_args={'check_same_thread': False}, echo=False)
    return engine


# 绑定了engine的session maker
Session = sessionmaker(bind=create_engine())


def create_session():
    return Session()
