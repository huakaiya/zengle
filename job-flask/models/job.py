# -*- codeing = utf-8 -*-
# Author: Redcomet
# QQ: 
# @Time: 2022/3/9 9:33
# @Author: Administrator
# @File: job.py
# @Desc:
import json
import jieba
from flask_marshmallow import Marshmallow
from base.core import db

ma = Marshmallow()

class Job(db.Model):
    __tablename__ = 'tb_job2'  #经过清洗后的招聘数据
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    number = db.Column(db.String(255))
    company_name = db.Column(db.String(255))
    position_name = db.Column(db.String(255))
    city = db.Column(db.String(255))
    salary0 = db.Column(db.DECIMAL)
    salary1 = db.Column(db.DECIMAL)
    degree = db.Column(db.String(255))
    company_logo = db.Column(db.String(512))
    url = db.Column(db.String(255))
    company_url = db.Column(db.String(255))
    education = db.Column(db.String(255))
    coattr = db.Column(db.String(255))
    cosize0 = db.Column(db.DECIMAL)
    cosize1 = db.Column(db.DECIMAL)
    worktime0 = db.Column(db.DECIMAL)
    worktime1 = db.Column(db.DECIMAL)
    welfare = db.Column(db.String(255))
    publish_time = db.Column(db.String(255))
    province = db.Column(db.String(50))
    flag = db.Column(db.Boolean, default=False)  # 添加 flag 字段，默认值为 False

class JobSchema(ma.Schema):
    class Meta:
        fields = ('id','number','company_name','position_name','city','salary0','salary1', \
                  'degree','company_logo','url','company_url','education','coattr','cosize0', \
                  'cosize1', 'worktime0', 'worktime1', 'welfare', 'publish_time','province' ,'flag' )

job_schema = JobSchema(many=True)

def getWords():
    records = db.session.query(Job).limit(5000).all()
    text = ""
    for i in records:
        # print(i.intro)  # 每一行
        if i.welfare is not None:   #需要修改词云分词的字段
            text = text + i.welfare

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


