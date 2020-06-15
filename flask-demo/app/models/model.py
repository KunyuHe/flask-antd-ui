from datetime import datetime
from sqlalchemy import ForeignKey, Table, Text, Column
from sqlalchemy.ext.declarative import declarative_base

from app.utils.core import db


class User(db.Model):
    """
    用户表
    """
    __tablename__ = 'tb_user'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)


class Customer(db.Model):
    """
    客户表
    """
    __tablename__ = "tb_customer"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    users = db.relationship('User', secondary=user_customer,
                            backref=db.backref('customers')
                            )
    incomes = db.relationship("Income", backref=db.backref("customer"))


# 用户-客户多对多
user_customer = db.Table('user_customer',
                         db.Column('user_id', db.Integer,
                                   db.ForeignKey('tb_user.id'),
                                   primary_key=True),
                         db.Column('customer_id', db.Integer,
                                   db.ForeignKey('tb_customer.id'),
                                   primary_key=True)
                         )


class Income(db.Model):
    """
    收入表
    """
    __tablename__ = "tb_income"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("tb_customer.id"))
    date = db.Column(db.Date, nullable=False)


class Trade(db.Model):
    """
    交易表
    """
    __tablename__ = "tb_trade"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.Integer, nullable=False)


class UserLoginMethod(db.Model):
    """
    用户登陆验证表
    """
    __tablename__ = 'user_login_method'
    id = db.Column(db.Integer, autoincrement=True,
                   primary_key=True)  # 用户登陆方式主键ID
    user_id = db.Column(db.Integer, nullable=False)  # 用户主键ID
    login_method = db.Column(db.String(36), nullable=False)  # 用户登陆方式，WX微信，P手机
    identification = db.Column(db.String(36), nullable=False)  # 用户登陆标识，微信ID或手机号
    access_code = db.Column(db.String(36), nullable=True)  # 用户登陆通行码，密码或token
