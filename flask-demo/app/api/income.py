# coding:utf-8
"""
规则说明:
调用单表接口需要指明支持的请求方法(GET,POST,PUT,DELETE),如果未指定，默认不注册该单表接口.
可以重新自定义的单表接口请求方式的处理逻辑

"""
from app.api.base import Service
from app.models.model import *


class IncomeAPI(Service):
    """
    用户与客户关系接口
    """
    __model__ = Income

    # 指定需要启用的请求方法
    __methods__ = ["GET", "POST", "PUT", "DELETE"]

    service_name = 'income'
