# coding: utf-8
from logger import logger
from . import create_engine, Base


def start_init():
    try:
        logger.info("start create database.")
        Base.metadata.create_all(create_engine())
        logger.info("the database create ok!")
    except Exception as e:
        logger.error(e)

