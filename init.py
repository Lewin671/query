# coding: utf-8
from config import BASE_PATH, SOUND_DIR, LOGGER_URI, DATABASE_URI
import os


def init():
    # 检测是否初始化
    data_path = os.path.join(BASE_PATH, "data")

    if not os.path.exists(data_path):
        # 创建data文件夹
        os.mkdir(data_path)

    # 创建声音目录
    if not os.path.exists(SOUND_DIR):
        os.mkdir(SOUND_DIR)

    # 创建日志文件
    if not os.path.exists(LOGGER_URI):
        file = open(LOGGER_URI, 'w')
        file.close()

    # 初始化数据库
    if not os.path.exists(DATABASE_URI):
        from models import init_db
        init_db.start_init()


init()
