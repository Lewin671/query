# coding: utf-8
from sqlalchemy import Column, String, ForeignKey, Integer

from . import Base


class Sentence(Base):
    __tablename__ = "sentence"
    id = Column(Integer, primary_key=True, autoincrement=True)
    en = Column(String, nullable=False)
    cn = Column(String, nullable=False)
    word_id = Column(Integer, ForeignKey('word.id'))
