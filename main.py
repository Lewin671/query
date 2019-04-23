from models import create_session,word,sentence
from config import SOUND_DIR,DISPLAY_SOUND,DISPLAY_TYPE
from logger import logger
from crawl import downloads
import threading

import os
import time
import sys

fmt = '\033[0;3{}m{}\033[0m'.format

BLACK  = 0#黑
RED    = 1#红
GREEN  = 2#绿
YELLOW = 3#棕
BLUE   = 4#蓝
PURPLE = 5#紫
CYAN   = 6#青
GRAY   = 7#灰


def display_music(path):
    try:
        import pygame
        pygame.mixer.init()
        track = pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        time.sleep(1)  # 播放5秒
        pygame.mixer.music.stop()  # 停止播放
    except:
        pass



def query(w):
    session = create_session()


    word_item = session.query(word.Word).filter_by(origin=w.strip()).first()

    if word_item is None:
        downloads.crawl(w)

    # retry
    word_item = session.query(word.Word).filter_by(origin=w.strip()).first()

    if word_item is None or word_item.translated is None or word_item.translated == "":
        print(fmt(RED,"sorry, no this word"))
        return

    print(fmt(YELLOW,word_item.origin))

    print(fmt(GREEN,word_item.phonetic))
    print(fmt(CYAN,word_item.translated.strip(','),end=""))

    for i,sentence in enumerate(word_item.sentences):
        if sentence is not None and sentence.en.strip() != "":
            print(fmt(GRAY,str(i+1)+"."),fmt(YELLOW,sentence.en))
            print(fmt(PURPLE,sentence.cn))

    logger.info("query word: {}".format(w))

if __name__=="__main__":

    if len(sys.argv) <= 1:
        print("usage: query [word]")

    else:
        queried_word = " ".join(sys.argv[1:])
        query(queried_word)

        if DISPLAY_SOUND:

            path = str()
            if DISPLAY_SOUND=="us":
                path = os.path.join(SOUND_DIR, queried_word+"_us.mp3")
            else:
                path = os.path.join(SOUND_DIR, queried_word+"_us.mp3")


            if not os.path.exists(path):
                downloads.crawl(queried_word)

            sound_thread = threading.Thread(target=display_music,args=(path,))
            sound_thread.start()
