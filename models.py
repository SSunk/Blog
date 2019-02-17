from exts import db
from datetime import datetime


class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(50),primary_key=True)
    password = db.Column(db.String(100),nullable=False)

class Article(db.Model):
    __tablename__='Article'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    biaoti = db.Column(db.String(100),primary_key=True)
    syzs = db.Column(db.String(200),nullable=True)
    fmdz = db.Column(db.String(500),nullable=True)
    nrdz = db.Column(db.String(500),nullable=True)
    neirong = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

class Liuyan(db.Model):
    __tablename__ = 'Liuyan'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name  = db.Column(db.String(50),primary_key=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
