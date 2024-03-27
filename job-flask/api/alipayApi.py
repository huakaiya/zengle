# -*- codeing = utf-8 -*-
# Author: Redcomet
# QQ: 
# @Time: 2022/3/10 16:12
# @Author: Administrator
# @File: alipay.py
# @Desc:

from alipay import AliPay
from flask import Blueprint, redirect

payBp = Blueprint("alipay", __name__)

@payBp.route('/testpay')
def testpay():
    order_numbering = "999999"
    order_total = 10.0
    # 个人私钥
    app_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
        -----END RSA PRIVATE KEY-----"""
    # 支付宝公钥
    alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
        -----END PUBLIC KEY-----"""

    alipay = AliPay(
        appid="2016092500594263",  # 第3步中的APPID
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",
        debug=False
    )

    # 电脑网站支付
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_numbering,  # 你自己生成的订单编号, 字符串格式
        total_amount=order_total,  # 订单总金额, 字符串格式
        subject="生鲜",  # 订单主题,可随便写
        return_url="",  # 支付完成后要跳转的页面, 完整的url地址,包括域名
        notify_url=None  # 可选, 不填则使用默认notify url
    )
    url = "https://openapi.alipaydev.com/gateway.do?" + order_string
    return redirect(url)


