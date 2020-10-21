# coding: utf-8
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship

from . import Base


class Word(Base):
    __tablename__ = "word"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 每一个单词都有一个唯一的id标识

    origin = Column(String, nullable=False, unique=True)  # 每一个单词都有原来的text，这里叫做origin

    phonetic = Column(String)  # 音标

    translated = Column(String, nullable=False)  # 翻译后的意思，包括词性和意思，如"vt. 好的，优秀的“

    sentences = relationship("Sentence", backref="word", cascade="all, delete, delete-orphan")  # 例句

    # 统计查词次数
    cnt = Column(Integer, default=0)

    # 是否学会?
    learned = Column(Boolean,default=False)

    def __repr__(self):
        return "Word(origin text is %s)" % (self.origin)
