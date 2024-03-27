# -*- codeing = utf-8 -*-
# Author: Redcomet
# QQ: 81040295
# @Time :2022/2/15 15:13
# @Author: Administrator
# @File :code.py.py

class ResponseCode(object):
    SUCCESS = 0  # 成功
    FAIL = -1  # 失败
    NO_RESOURCE_FOUND = 40001  # 未找到资源
    INVALID_PARAMETER = 40002  # 参数无效
    ACCOUNT_OR_PASS_WORD_ERR = 40003  # 账户或密码错误
    USERNAME_ALREADY_EXIST = 50001 # 账户名已存在


class ResponseMessage(object):
    SUCCESS = "成功"
    FAIL =  "失败"
    NO_RESOURCE_FOUND =  "未找到资源"
    INVALID_PARAMETER =  "参数无效"
    ACCOUNT_OR_PASS_WORD_ERR =  "账户或密码错误"
    USERNAME_ALREADY_EXIST = "账户名已存在"