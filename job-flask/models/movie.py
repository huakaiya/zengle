# -*- codeing = utf-8 -*-
# Author: Redcomet
# QQ: 
# @Time: 2022/2/18 17:06
# @Author: Administrator
# @File: movieApi.py.py
# @Desc:
import json
import app
import jieba
from flask_marshmallow import Marshmallow

from base.core import db
ma = Marshmallow(app)

class Movie(db.Model):
    __tablename__ = 'tb_movie'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    url = db.Column(db.String(255))
    img = db.Column(db.String(255))
    name = db.Column(db.String(255))
    name_eng = db.Column(db.String(255))
    rate = db.Column(db.DECIMAL)
    comment_num = db.Column(db.Integer)
    director = db.Column(db.String(255))
    actor = db.Column(db.String(255))
    myear = db.Column(db.String(255))
    nation = db.Column(db.String(255))
    type = db.Column(db.String(255))
    intro = db.Column(db.String(255))  #

class MovieSchema(ma.Schema):
    class Meta:
        # fields = ('url','img','name')
        fields = ('id','url','img','name','name_eng','rate','comment_num','director','actor','myear','nation','type','intro')

movie_schema = MovieSchema(many=True)

def getWords():
    intros = db.session.query(Movie).all()
    text = ""
    for i in intros:
        # print(i.intro)  # 每一行
        if i.intro is not None:
            text = text + i.intro

    word_count = dict()
    words = jieba.cut(text)
    for word in words:
        if word not in word_count:
            word_count[word] = 1
        else:
            word_count[word] += 1

    # 词频顺序进行排序，以元祖形式存储
    word_count_sorted = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    # print(word_count_sorted)

    # 过滤结果中的标点符号和单词
    word_count_sorted = filter(lambda x: len(x[0]) > 1, word_count_sorted)
    # print(word_count_sorted)

    # 元组转json
    result = json.dumps(dict(word_count_sorted), ensure_ascii=False)
    # result = json.dumps(dict(word_count_sorted), ensure_ascii=False)
    print(json.loads(result))
    result = json.loads(result)
    return result
