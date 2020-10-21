# coding: utf-8
# from lxml import etree
import json
import os
from urllib.request import urlretrieve

import lxml.html
import requests

from config import SOUND_DIR, MAX_SENTENCE_NUMBER, DISPLAY_SOUND
from models import word, sentence, create_session

etree = lxml.html.etree
url = "http://www.iciba.com"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
}

json_path = "/html/body/script/text()"


# 下载这个单词的json文件
def download_json_obj(w: str):
    response = requests.get(url + "/" + w, headers=headers)
    html = etree.HTML(response.text)

    # json数据
    data = ",".join(html.xpath(json_path))
    return json.loads(data)


# 解析json文件，得到一个单词对象
def crawl(queried_word: str) -> word.Word:
    global ph_en, ph_am, ph_en_mp3, ph_am_mp3
    ph_en = ph_am = ph_en_mp3 = ph_am_mp3 = None

    word_item = word.Word()
    word_item.origin = queried_word

    data = download_json_obj(queried_word)

    # 解码python json格式

    wordInfo = data["props"]['initialDvaState']['word']['wordInfo']

    # 基本信息
    try:
        symbol = wordInfo["baesInfo"]['symbols'][0]
    except Exception as e:  # 没有找到这个单词
        return

    # 音标
    if "ph_en" in symbol:
        ph_en = symbol['ph_en']
    if "ph_am" in symbol:
        ph_am = symbol['ph_am']
    if "ph_en_mp3" in symbol:
        ph_en_mp3 = symbol['ph_en_mp3']
    if "ph_am_mp3" in symbol:
        ph_am_mp3 = symbol['ph_am_mp3']
    # 音标不为None，并且非空
    if ph_en is not None and ph_am is not None \
            and ph_en != "" and ph_am != "":
        phonetic = '[' + ph_en + '], [' + ph_am + ']'
        word_item.phonetic = phonetic

    # 读音
    if DISPLAY_SOUND and ph_en_mp3 is not None and ph_am_mp3 is not None:
        sounds = [ph_en_mp3, ph_am_mp3]
        try:
            filename = queried_word.replace(" ", "_")
            urlretrieve(sounds[0], filename=os.path.join(SOUND_DIR, filename + "_uk.mp3"))
            urlretrieve(sounds[1], filename=os.path.join(SOUND_DIR, filename + "_us.mp3"))
        except Exception as e:  # 没有声音
            print(e)

    # 单词意思
    parts = symbol['parts']

    translated = str()

    l = len(parts)
    for i in range(l):
        part = parts[i]
        attr = part['part']
        meaning = ",".join(part['means'])
        translated = translated + attr + meaning
        if i != l-1:
            translated = translated + "\n"

    word_item.translated = translated

    # 例句
    new_sentence = wordInfo['new_sentence']
    en_sentence = list()
    cn_sentence = list()

    # 每个意思都选取一个例句
    for s in new_sentence:
        en_sentence.append(s['sentences'][0]['en'])
        cn_sentence.append(s['sentences'][0]['cn'])

    sentences = list()

    for i in range(len(en_sentence)):
        if i >= MAX_SENTENCE_NUMBER:
            break
        s = sentence.Sentence()
        s.en = en_sentence[i]
        s.cn = cn_sentence[i]
        sentences.append(s)
    word_item.sentences = sentences
    return word_item


# 将单词对象保存到数据库
def save_word_item(word_item: word.Word):
    session = create_session()
    try:
        session.add(word_item)
        session.commit()
    except Exception as e:
        session.rollback()


# 根据单词字符查询，并保存到数据库
def save_word(queried_word: str):
    word_item = crawl(queried_word)
    save_word_item(word_item)