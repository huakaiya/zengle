# -*- codeing = utf-8 -*-
# Author: Redcomet
# QQ: 
# @Time :2022/2/16 11:23
# @Author: Administrator
# @File :userApi.py
import json
from flask import Blueprint, request, flash, session, jsonify
from base.code import ResponseCode, ResponseMessage
from base.response import ResMsg
from base.core import db
from models.model import valid_login, valid_register, User, user_schema

userBp = Blueprint("user", __name__)

@userBp.route( '/userinfo', methods=["POST"])
def userinfo():
    res = ResMsg()
    username = request.json['username']
    user = User.query.filter(User.username == username).first()
    print(user)
    # data = dict(zip(user.keys(), user))
    data = user_schema.dump(user)
    res.update(code=ResponseCode.SUCCESS, data=data)
    return res.data

# 登录接口，登录后需要返回用户信息给前端
@userBp.route( '/login', methods=["POST"])
def login():
    res = ResMsg()
    username = request.json['username']
    password = request.json['password']
    if valid_login(username, password):
        # flash(username + "登录成功")
        session['username'] = username
        # userId = db.session.query(User.id).filter(User.username==username).first()
        user = db.session.query(User).filter(User.username == username).first()
        json = user_schema.dump(user)
        # print(userId)
        res.update(code=ResponseCode.SUCCESS,msg=ResponseMessage.SUCCESS,data=json)
    else:
        res.update(code=ResponseCode.ACCOUNT_OR_PASS_WORD_ERR,msg=ResponseMessage.ACCOUNT_OR_PASS_WORD_ERR)
    return res.data

@userBp.route( '/logout')
def logout():
    res = ResMsg()
    session.pop('username', None)
    return res.data

@userBp.route( '/get/<id>', methods=["GET"])
def get(id):
    res = ResMsg()
    user = User.query.filter(User.id == id).first()
    print(user)
    data = user_schema.dump(user)
    res.update(code=ResponseCode.SUCCESS, data=data)
    return res.data

@userBp.route('/register', methods=["POST"])
def register():
    res = ResMsg()
    username = request.json['username']
    password = request.json['password']
    realname = request.json['realname']
    if valid_register(username):
        user = User(username=username, password=password, realname=realname)
        db.session.add(user)
        db.session.commit()
        res.update(code=ResponseCode.SUCCESS)
    else:
        res.update(code=ResponseCode.USERNAME_ALREADY_EXIST, msg=ResponseMessage.USERNAME_ALREADY_EXIST)
    return res.data

@userBp.route('/idconfirm', methods=["POST"])
def idconfirm():
    res = ResMsg()
    id = request.json['id']
    idno = request.json['idno']
    realname = request.json['realname']
    db.session.query(User).filter(User.id == id).update({"idno": idno, "realname": realname})
    db.session.commit()
    res.update(code=ResponseCode.SUCCESS)
    return res.data

@userBp.route('/update', methods=["POST"])
def update():
    res = ResMsg()
    id = request.json['id']
    # realname = request.json['realname']
    phone = request.json['phone']
    email = request.json['email']
    avatar = request.json['avatar']
    intro = request.json['intro']
    addr = request.json['addr']
    age = request.json['age']

    db.session.query(User).filter(User.id == id).update({"phone":phone, \
                                                         "email":email,"avatar":avatar,"intro":intro,\
                                                         "addr":addr,"age":age})
    db.session.commit()
    res.update(code=ResponseCode.SUCCESS)
    return res.data