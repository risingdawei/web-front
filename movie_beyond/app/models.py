# -*- coding: utf-8 -*-
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)
# 后面的相应名字是，用户名、密码、地址、端口以及库名
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:LYP91Nmysqllp@127.0.0.1:3306/movie"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)


#会员
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True) # 编号
    name = db.Column(db.String(100), unique=True) # 昵称
    pwd = db.Column(db.String(100)) # 密码
    email = db.Column(db.String(100), unique=True) # 邮箱
    phone = db.Column(db.String(11), unique=True) # 手机号码
    info = db.Column(db.Text) # 个性简介
    face = db.Column(db.String(255),unique=True)# 头像
    addtime = db.Column(db.DateTime,index=True,default=datetime.now) # 登录时间
    uuid = db.Column(db.String(255), unique=True) # 唯一标志符
    userlogs = db.relationship('Userlog', backref='user') # 会员日志外键关系关联
    comments = db.relationship('Comment', backref='user')  # 评论日志外键关系关联
    moviecols = db.relationship('Moviecol', backref='user')  # 收藏日志外键关系关联

    def __repr__(self):
        return "<User %r>" % self.name


#会员登录日志
class Userlog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.Integer, primary_key=True) # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # 所属会员
    ip = db.Column(db.String(100)) # 登录IP
    addtime = db.Column(db.DateTime,index=True,default=datetime.now) # 登录时间

    def __repr__(self):
        return "<Userlog %r>" % self.id

#标签
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)   # 编号
    name = db.Column(db.String(100), unique=True)   # 标题
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)    # 添加时间
    movies = db.relationship("Movie", backref='tag')   # 电影外键关系关联

    def __repr__(self):
        return "<Tag %r>" % self.name

#电影
class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)   # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    url = db.Column(db.Integer, primary_key=True)   # 地址
    info = db.Column(db.Text)   # 简介
    logo = db.Column(db.String(255), unique=True)  # 封面
    star = db.Column(db.SmallInteger)    # 星级
    playnum = db.Column(db.BigInteger)    # 播放量
    commentnum = db.Column(db.BigInteger)    # 评论量
    tag_id = db.Column(db.Integer,db.ForeignKey('tag.id'))    # 所属标签
    area = db.Column(db.String(255))    # 上映地区
    release_time = db.Column(db.Date)    # 上映时间
    length = db.Column(db.String(100))    # 播放时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)    # 添加时间
    comments = db.relationship("Comment", backref='movie')  # 评论外键关系关联
    moviecols = db.relationship("Moviecol", backref='movie')  # 收藏外键关系关联

    def __repr__(self):
        return "<Movie %r>" % self.title


# 上映预告
class Preview(db.Model):
    __tablename__ = "preview"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    logo = db.Column(db.String(255), unique=True)  # 封面
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Preview %r>" % self.title


# 评论
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    content = db.Column(db.Text)  # 内容
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Comment %r>" % self.id

#电影收藏
class Moviecol(db.Model):
    __tablename__ = "moviecol"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Moviecol %r>" % self.id

#权限
class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    url = db.Column(db.String(255), unique=True)  # 地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Auth %r>" % self.name

#角色
class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    auths = db.Column(db.String(600))  # 地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Role %r>" % self.name

#管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 昵称
    pwd = db.Column(db.String(100))  # 密码
    is_super = db.Column(db.SmallInteger)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    adminlogs = db.relationship("Adminlog", backref='admin')  # 管理员登录日志外键关系关联
    oplogs = db.relationship("Oplog", backref='admin')  # 操作日志外键关系关联

    def __repr__(self):
        return "<Admin %r>" % self.name

#管理员登录日志
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True) # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id')) # 所属会员
    ip = db.Column(db.String(100)) # 登录IP
    addtime = db.Column(db.DateTime,index=True,default=datetime.now) # 登录时间

    def __repr__(self):
        return "<Adminlog %r>" % self.id

#操作日志
class Oplog(db.Model):
    __tablename__ = "oplog"
    id = db.Column(db.Integer, primary_key=True) # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id')) # 所属会员
    ip = db.Column(db.String(100)) # 登录IP
    reason = db.Column(db.String(600))  # 操作日志
    addtime = db.Column(db.DateTime,index=True,default=datetime.now) # 登录时间

    def __repr__(self):
        return "<Oplog %r>" % self.id

if __name__ == "__main__":
    from werkzeug.security import generate_password_hash

    admin = Admin(
        name = "daweidemovie33",
        pwd = generate_password_hash("daweidemovie33"),
        is_super = 0,
        role_id = 1
    )
    db.session.add(admin)
    db.session.commit()
    # role = Role(
    #     name="superuser",
    #     auths=""
    # )
    # db.session.add(role)
    # db.session.commit()

    # db.create_all()

