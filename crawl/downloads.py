import requests
#from lxml import etree
import lxml.html
etree = lxml.html.etree
import re
from bs4 import BeautifulSoup
from models import word,sentence,create_session
from urllib.request import urlretrieve
from config import SOUND_DIR
import os
from logger import logger

url = "http://www.iciba.com"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
}


def crawl(w):
    word_item = word.Word()
    word_item.origin = w

    response = requests.get(url + "/" + w, headers=headers)
    html = etree.HTML(response.text)

    # 音标
    phonetic = ",".join(html.xpath('/html/body/div/div/div/div/div/div/div/div/div/span/span/text()'))
    word_item.phonetic = phonetic


    # 读音
    pattern = re.compile(r"http.*.mp3")
    sounds = [re.search(pattern,sound).group() for sound in
              html.xpath('/html/body/div/div/div/div/div/div/div/div/div/span/i/@ms-on-mouseover')]


    try:
        urlretrieve(sounds[0],filename=os.path.join(SOUND_DIR,w+"_uk.mp3"))
        urlretrieve(sounds[1], filename=os.path.join(SOUND_DIR, w + "_us.mp3"))
    except Exception as e:
        pass

    meaning_blocks = html.xpath('/html/body/div/div/div/div/div/div/ul/li')

    translated = str()

    for item in meaning_blocks:
        attr = item.xpath('./span[@class="prop"]/text()')
        meaning = item.xpath('./p/span/text()')

        if len(attr)==0:
            attr.append("")

        translated = translated + str(attr[0]) + " " + " ".join(meaning) + "\n"

    word_item.translated = translated

    #print(phonetic,sounds)

    # 例句
    en_sentence = list()
    cn_sentence = list()
    soup = BeautifulSoup(response.text, 'html.parser')
    cnt = 1
    example = soup.select('.prep-order > .text-sentence p')
    for item in example:
        if cnt > 6:
            break
        if cnt % 2 == 0:
            cn_sentence.append(item.text.strip())
        else:
            en_sentence.append(item.text.strip())
        cnt += 1

    sentences = list()

    for i in range(len(en_sentence)):
        s = sentence.Sentence()
        s.en = en_sentence[i]
        s.cn = cn_sentence[i]
        sentences.append(s)

    try:
        word_item.sentences = sentences
        session = create_session()
        session.add(word_item)
        session.commit()
    except:
        pass
