import os
import time

from flask import Flask, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from werkzeug.utils import secure_filename, redirect

from api.alipayApi import payBp
from api.baiduApi import idocr
from base.core import JSONEncoder
from base.response import ResMsg
from api.testApi import bp

import logging

app = Flask(__name__)
app.register_blueprint(bp, url_prefix='/test')
# app.register_blueprint(movieBp, url_prefix='/movie')
app.register_blueprint(payBp, url_prefix='/alipay')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/flask_job'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = 'KJDFLSjfldskj'

UPLOAD_FOLDER="upload"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt','png','jpg','xls','JPG','PNG','gif','GIF'])

# 日志系统配置
handler = logging.FileHandler('error.log', encoding='UTF-8')
logging_format = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)

# 返回json格式转换
app.json_encoder = JSONEncoder

db = SQLAlchemy(app)
ma = Marshmallow(app)

from api.userApi import userBp
from api.jobApi import jobBp

app.register_blueprint(userBp, url_prefix='/user')
app.register_blueprint(jobBp, url_prefix='/job')

@app.route('/test')
def test():  # put application's code here
    res = ResMsg()
    test_dict = dict(name="zhang", age=19)
    res.update(data=test_dict, code=0)
    return res.data

@app.errorhandler(500)
def special_exception_handler(error):
    app.logger.error(error)
    return '请联系管理员', 500

#判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@app.route('/file/upload', methods=['POST'], strict_slashes=False)
def api_upload():
    res = ResMsg()
    file_dir=os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['myfile']
    if f and allowed_file(f.filename):
        fname = f.filename
        # fname = secure_filename(f.filename)
        print(fname)
        ext = fname.rsplit('.', 1)[1]
        unix_time = int(time.time())
        new_filename = str(unix_time)+'.'+ext
        f.save(os.path.join(file_dir, new_filename))
    res.update(data=new_filename, code=0)
    return res.data

@app.route('/file/idocr', methods=['POST'], strict_slashes=False)
def api_id_ocr():
    res = ResMsg()
    file_dir=os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['myfile']
    if f and allowed_file(f.filename):
        fname = f.filename
        # fname = secure_filename(f.filename)  有中文这个会有问题
        # print(fname)
        ext = fname.rsplit('.', 1)[1]
        unix_time = int(time.time())
        new_filename = str(unix_time)+'.'+ext
        f.save(os.path.join(file_dir, new_filename))
        idno = idocr(new_filename)[0]
        name = idocr(new_filename)[1]
    res.update(data=dict(idno=idno,pic=new_filename,name=name), code=0)
    return res.data

@app.route('/file/download/<filename>/')
def api_download(filename):
    # print('下载..' + filename)
    return send_from_directory('upload', filename, as_attachment=False)



if __name__ == '__main__':
    # app.run(debug=True,host='0.0.0.0',port=5000)
   app.run()
