# -*- codeing = utf-8 -*-
# Author: Redcomet
# QQ: 
# @Time: 2022/3/10 16:12
# @Author: Administrator
# @File: fileApi.py
# @Desc:
import os

from flask import Flask, send_from_directory

app = Flask(__name__)
UPLOAD_FOLDER="upload"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt','png','jpg','xls','JPG','PNG','gif','GIF'])

#判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@app.route('/file/download/<filename>/')
def api_download(filename):
    if os.file.isfile(os.path.join('upload', filename)):
        return send_from_directory('upload', filename, as_attachment=True)


