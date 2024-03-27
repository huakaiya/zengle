

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/flask_douban'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)

class MovieInfo(db.Model):
    __tablename__ = 'tb_movie'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    type = db.Column(db.String(255))
    nation = db.Column(db.String(255))

infos = db.session.query(MovieInfo).all()

types = []
for i in infos:
    if i.type is not None :
        for t in i.type.split(" "):
            types.append(t)
print(list(set(types)))

nations = []
for i in infos:
    x = i.nation
    for t in x.split(" "):
        nations.append(t)
print(list(set(nations)))

