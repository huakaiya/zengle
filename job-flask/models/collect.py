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

class Collect(db.Model):
    __tablename__ = 'collect'
    jobid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, nullable=True)  # 这里可能需要根据你的具体用户表进行关联，这里假设userid可以为空

    # 添加外键约束
    # 如果有用户表，你可以根据需要添加外键约束，示例代码如下：
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # 可以添加一些其他的字段，比如收藏时间等

    def __repr__(self):
        return f"Collect(jobid={self.jobid}, userid={self.userid})"
    userid = db.Column(db.Integer)


