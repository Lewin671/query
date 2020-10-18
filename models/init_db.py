# coding: utf-8
from logger import logger
from . import create_engine, Base

# 创建数据库
def start_init():
    # 创建
    try:
        from .word import Word
        from .sentence import Sentence
        logger.info("start create database.")
        Base.metadata.create_all(create_engine())
        logger.info("the database create ok!")
    except Exception as e:
        logger.error("创建错误")
        logger.error(e)
