# coding: utf-8
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import *


def create_engine():
    engine = sqlalchemy.create_engine('sqlite:///' + DATABASE_URI,connect_args={'check_same_thread':False},echo=False)
    return engine


Session = sessionmaker(bind=create_engine())

Base = declarative_base()


def create_session():
    return Session()