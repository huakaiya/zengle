
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DECIMAL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import DOUBLE
from base import DB_URI

engine = create_engine(DB_URI)
Base = declarative_base(engine)  # SQLORM基类
session = sessionmaker(engine)()  # 构建session对象

class Tour(Base):
    __tablename__ = 'tb_tour'  # 表名
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(500))
    grade = Column(String(20))
    address = Column(String(500))
    intro = Column(String(500))
    hot = Column(DOUBLE)
    price = Column(DOUBLE)
    msold = Column(Integer)
    lng = Column(DOUBLE)
    lat = Column(DOUBLE)
    img = Column(String(500))
    province = Column(String(90))
    city = Column(String(90))
    district = Column(String(90))

    def __init__(self, name, grade, address, intro, hot, price, msold, lng, lat, img, province, city, district):
        self.name = name
        self.grade = grade
        self.address = address
        self.intro = intro
        self.hot = hot
        self.price = price
        self.msold = msold
        self.lng = lng
        self.lat = lat
        self.img = img
        self.province = province
        self.city = city
        self.district = district

def save(tour):
    session.add(tour)  # 添加到session
    session.commit()  # 提交到数据库

# tour = Tour(name='圆通寺')  # 创建一个tour对象
# session.add(tour)  # 添加到session
# session.commit()  # 提交到数据库