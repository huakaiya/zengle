
import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import jieba
import jieba.analyse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/flask_douban'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)

class MovieIntro(db.Model):
    __tablename__ = 'tb_movie'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    intro = db.Column(db.String(255))  # 用户姓名

intros = db.session.query(MovieIntro).all()
text = ""
for i in intros:
    # print(i.intro)  # 每一行
    if i.intro is not None :
        text = text + i.intro
# print(text)

# cut = jieba.cut(text)
# string = ' '.join(cut)
# print(string)

# 主题词
# tags = jieba.analyse.extract_tags(text)
# print(tags)
#
# for t in tags:
#     word_lst.append(t)

word_count = dict()
words = jieba.cut(text)
for word in words:
    if word not in word_count:
        word_count[word] = 1
    else:
        word_count[word] += 1

# 词频顺序进行排序，以元祖形式存储
word_count_sorted = sorted(word_count.items(), key=lambda x:x[1], reverse=True)
print(word_count_sorted)

# 过滤结果中的标点符号和单词
word_count_sorted = filter(lambda x: len(x[0]) > 1, word_count_sorted)
print(word_count_sorted)

# 元组转json
result = json.dumps(dict(word_count_sorted), ensure_ascii=False)
print(result)