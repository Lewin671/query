# coding: utf-8
import json

if __name__ == "__main__":
    with open('data.json', 'r') as f:
        data = json.load(f)
    wordInfo = data["props"]['initialDvaState']['word']['wordInfo']

    # 基本信息
    symbol = wordInfo["baesInfo"]['symbols'][0]

    # 音标
    ph_en = symbol['ph_en']
    ph_am = symbol['ph_am']
    ph_en_mp3 = symbol['ph_en_mp3']
    ph_am_mp3 = symbol['ph_am_mp3']

    # 单词意思
    parts = symbol['parts']
    for part in parts:
        print(part)

    # 例句
    new_sentence = wordInfo['new_sentence']

    # 每个意思都选取一个例句
    for sentence in new_sentence:
        print(sentence['sentences'][0]['en'])
        print(sentence['sentences'][0]['cn'])
