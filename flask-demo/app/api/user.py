import logging
from flask import Blueprint, session, jsonify, request, current_app
from sqlalchemy import and_, text

from app.models.model import User, Customer
from app.utils.auth import Auth, login_required
from app.utils.core import db
from app.utils.emailsender import EmailSender
from app.utils.response import ResMsg, ResponseCode
from app.utils.util import model_to_dict
from app.utils.util import route, EmailTool, model_to_dict

bp = Blueprint("api_user", __name__, url_prefix='/user')
logger = logging.getLogger(__name__)


@route(bp, '/login', methods=["POST"])
def login():
    """
    登陆成功获取到数据获取token和刷新token
    :return:
    """
    res = ResMsg()
    obj = request.get_json(force=True)

    user_name = obj.get("username")
    user_password = obj.get("password")
    # 未获取到参数或参数不存在
    if not obj or not user_name or not user_password:
        res.update(code=ResponseCode.InvalidParameter)
        return res.data

    user = db.session.query(User).filter(User.username == user_name).first()
    if user and user.password == user_password:
        # 生成数据获取token和刷新token
        access_token, refresh_token = Auth.encode_auth_token(user_id=user_name)

        data = {"access_token": access_token.decode("utf-8"),
                "refresh_token": refresh_token.decode("utf-8"),
                "user": model_to_dict(user)
                }
        res.update(data=data)
        return res.data

    else:
        res.update(code=ResponseCode.AccountOrPassWordErr)
        return res.data


@route(bp, '/register', methods=["POST"])
def register():
    """
    注册
    :return:
    """
    res = ResMsg()
    obj = request.get_json(force=True)

    user_name = obj.get("username")
    user_email = obj.get("email")
    if not obj or not user_name or not user_email:
        res.update(code=ResponseCode.InvalidParameter)
        return res.data

    email_qualify = EmailTool.check_email(user_email)
    if not email_qualify:
        res.update(code=ResponseCode.InvalidEmail)
        return res.data

    same_user_count = db.session.query(User).filter(
        User.username == user_name).count()
    if same_user_count != 0:
        res.update(code=ResponseCode.RepeatUserName)
        return res.data

    register_user = User(username=user_name, password=obj.get("password"),
                         phone=obj.get("phone"),
                         email=obj.get("email"), address=obj.get("address"))
    db.session.add(register_user)
    db.session.commit()
    user_json = model_to_dict(register_user)
    res.update(data=user_json)

    return res.data


@route(bp, '/send', methods=["POST"])
@login_required
def send_email():
    """
    发送邮件
    :return:
    """
    res = ResMsg()

    user_name = session["user_name"]
    customer_id = request.form.get("customer_id")
    file = request.files['file']
    if not user_name or not customer_id or not file:
        res.update(code=ResponseCode.InvalidParameter)
        return res.data

    user = db.session.query(User).filter(User.username == user_name).first()
    customer = db.session.query(Customer).filter(
        Customer.id == customer_id).first()
    restult = EmailSender.send_email(customer.email, user.username, user.email,
                                     file.stream.read(), file.filename)

    if not restult:
        res.update(code=ResponseCode.SendEmailFailed)
        return res.data

    return res.data


@route(bp, '/customers', methods=["GET"])
@login_required
def get_user_customers():
    res = ResMsg()

    user_name = session["user_name"]
    if not user_name:
        res.update(ResponseCode.InvalidParameter)
        return res.data

    user_obj = db.session.query(User).filter(User.username == user_name).first()
    customers_json = []
    if user_obj and user_obj.customers:
        for customer_obj in user_obj.customers:
            incomes_json = []
            if customer_obj.incomes:
                incomes_json = model_to_dict(customer_obj.incomes)
            customer_json = model_to_dict(customer_obj)
            customer_json["incomes"] = incomes_json
            customers_json.append(customer_json)

    user = model_to_dict(user_obj)
    user["customers"] = customers_json
    res.update(data=user)

    return res.data


@route(bp, '/info', methods=["GET"])
@login_required
def get_user():
    res = ResMsg()

    obj = request.get_json(force=True)
    user_name = session["user_name"]
    if not obj or not user_name:
        res.update(ResponseCode.InvalidEmail)
        return res.data

    user = db.session.query(User).filter(User.username == user_name).first()
    customers = model_to_dict(user)
    res.update(data=customers)

    return res.data


@route(bp, '/testGetData', methods=["GET"])
@login_required
def test_get_data():
    """
    测试登陆保护下获取数据
    :return:
    """
    res = ResMsg()

    name = session.get("user_name")
    data = "{}，您好！".format(name)
    res.update(data=data)

    return res.data


@route(bp, '/RefreshToken', methods=["GET"])
def refresh_token():
    """
    刷新token，获取新的数据获取token
    :return:
    """
    res = ResMsg()

    refresh_token = request.args.get("refresh_token")
    if not refresh_token:
        res.update(code=ResponseCode.InvalidParameter)
        return res.data

    payload = Auth.decode_auth_token(refresh_token)
    # token被串改或过期
    if not payload:
        res.update(code=ResponseCode.PleaseSignIn)
        return res.data

    # 判断token正确性
    if "user_id" not in payload:
        res.update(code=ResponseCode.PleaseSignIn)
        return res.data

    # 获取新的token
    access_token = Auth.generate_access_token(user_id=payload["user_id"])
    data = {"access_token": access_token.decode("utf-8"),
            "refresh_token": refresh_token}
    res.update(data=data)

    return res.data
