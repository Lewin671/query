# coding: utf-8

import os

# 项目的根目录
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# 数据库地址
DATABASE_URI = os.path.join(BASE_PATH, "data/data.db")

# 日志的文件地址
LOGGER_URI = os.path.join(BASE_PATH, 'data/log.txt')

# 读音的地址
SOUND_DIR = os.path.join(BASE_PATH,"data/sounds")

# 是否选择有读音,默认是True
DISPLAY_SOUND = True

# 英式发音为"uk",美式发音为"us"
DISPLAY_TYPE = "us"
