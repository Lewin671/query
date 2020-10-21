# coding: utf-8
import os
import sys
import threading

from playsound import playsound
# 初始化需要这个
import init
from config import SOUND_DIR, DISPLAY_SOUND, BASE_PATH, LOGGER_URI
from crawl import downloads
from models import create_session, word, init_db
from logger import logger

# 打包需要用到这个
import sqlalchemy.ext.baked

Word = word.Word

fmt = '\033[0;3{}m{}\033[0m'.format

BLACK = 0  # 黑
RED = 1  # 红
GREEN = 2  # 绿
YELLOW = 3  # 棕
BLUE = 4  # 蓝
PURPLE = 5  # 紫
CYAN = 6  # 青
GRAY = 7  # 灰


def display_music(sound_path: str):
    if os.path.exists(sound_path):
        playsound(sound_path)


# 从数据库中检索出该单词
def query(w: str):
    session = create_session()

    word_item = session.query(word.Word).filter_by(origin=w.strip()).first()

    if word_item is None:
        downloads.save_word(w)

    # retry
    word_item = session.query(word.Word).filter_by(origin=w.strip()).first()

    if word_item is None or word_item.translated is None or word_item.translated == "":
        print(fmt(RED, "sorry, no this word"))
        return

    print(fmt(YELLOW, word_item.origin))

    # 中文没有音标
    if word_item.phonetic is not None:
        print(fmt(GREEN, word_item.phonetic))

    print(fmt(CYAN, word_item.translated.strip(','), end=""))
    print(fmt(CYAN, "查询次数:"), fmt(PURPLE, word_item.cnt + 1))

    for i, sentence in enumerate(word_item.sentences):
        if (sentence is not None) and (sentence.en.strip() != ""):
            print(fmt(GRAY, str(i + 1) + "."), fmt(YELLOW, sentence.en))
            print(fmt(PURPLE, sentence.cn))

    logger.info("query word: {}".format(w))

    # 播放声音
    if DISPLAY_SOUND:
        path = str()
        filename = queried_word.replace(" ", "_")
        if DISPLAY_SOUND == "us":
            path = os.path.join(SOUND_DIR, filename + "_us.mp3")
        else:
            path = os.path.join(SOUND_DIR, filename + "_us.mp3")

        if not os.path.exists(path):
            downloads.save_word(queried_word)

        sound_thread = threading.Thread(target=display_music, args=(path,), daemon=True)
        sound_thread.setDaemon(False)
        sound_thread.start()

    # 更新数据
    # session.query(Word).filter(Word.origin == w).update({"cnt": Word.cnt + 1})
    word_item.cnt = word_item.cnt + 1
    try:
        session.commit()
    except Exception as e:
        print(e)


# 从数据库中查询高频(未学会的)词汇
def show_high_frequency_words(n: int):
    session = create_session()
    words = session.query(Word) \
        .filter(Word.learned == False) \
        .order_by(Word.cnt.desc()) \
        .limit(n) \
        .all()

    for w in words:
        print(w.origin, w.cnt)


# 将learned字段取反
def set_learn_word(w: str):
    session = create_session()
    word_item = session.query(Word).filter(Word.origin == w).first()
    if word_item is None:
        print("该单词未查询过，无法设置其learned字段")
        return

    word_item.learned = not word_item.learned
    try:
        session.commit()
    except Exception as e:
        print(e)


# 查看学会的单词
def show_learned_words(n: str):
    session = create_session()
    for w in session.query(Word).filter(Word.learned == True).limit(n):
        print(w.origin)


# 输出帮助信息
def print_help():
    print("usage: query [option][word]")
    print("-sh: show high frequency words,[word] should be empty")
    print("-sl: show learned words,[word] should be empty")
    print("-l: learn the [word], meaning it will not be show by -sh")
    pass


if __name__ == "__main__":
    # sys.argv = ["", "test"]
    if len(sys.argv) <= 1:
        print("usage: query [word]")
    else:
        parameter = " ".join(sys.argv[1:])
        if parameter == "-h" or parameter == "--help":
            print_help()
            sys.exit(0)
        elif parameter == "-sh":
            show_high_frequency_words(10000)
            sys.exit(0)
        elif sys.argv[1] == "-l":
            set_learn_word(sys.argv[2])
            sys.exit(0)
        elif parameter == "-sl":
            show_learned_words(10000)
            sys.exit(0)

        queried_word = " ".join(sys.argv[1:])
        query(queried_word)
