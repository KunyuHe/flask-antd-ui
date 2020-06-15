import json
import logging
from flask import Blueprint, session
from flask import request

from app.models.model import User, Customer, Income
from app.utils.auth import login_required
from app.utils.core import db
from app.utils.response import ResponseCode, ResMsg
from app.utils.util import route, model_to_dict

bp = Blueprint("api_customer", __name__, url_prefix='/customer')
logger = logging.getLogger(__name__)


@route(bp, '/add', methods=["POST"])
@login_required
def add_customer():
    """
    添加客户
    :return:
    """
    res = ResMsg()
    try:
        customer = request.get_json(force=True)
        user_name = session["user_name"]
        user = db.session.query(User).filter(User.username == user_name).first()
        if not customer or not user:
            res.update(code=ResponseCode.InvalidParameter)
            return res.data

        customer_count = db.session.query(Customer).filter(
            Customer.name == customer.get("name")).count()
        if customer_count != 0:
            res.update(code=ResponseCode.RepeatUserName)
            return res.data

        customer_obj = Customer()
        customer_obj.name = customer.get("name")
        customer_obj.email = customer.get("email")
        customer_obj.users.append(user)

        db.session.add(customer_obj)
        db.session.commit()
        res.update(data=model_to_dict(customer_obj))

    except Exception as ex:
        logging.error(ex)
        res.update(code=ResponseCode.Fail)

    return res.data


@route(bp, '/all', methods=["GET"])
@login_required
def get_all_customers():
    res = ResMsg()
    customers = db.session.query(Customer).filter().all()
    customers_json = []
    for customer in customers:
        incomes_dic = model_to_dict(customer.incomes)
        customer_dic = model_to_dict(customer)
        customer_dic["incomes"] = incomes_dic
        customers_json.append(customer_dic)

    res.update(data=customers_json)

    return res.data


@route(bp, '/income', methods=["POST"])
@login_required
def get_customer_income():
    res = ResMsg()
    obj = request.get_json(force=True)
    customer_id = obj.get("customer_id")

    if not obj or not customer_id:
        res.update(ResponseCode.InvalidParameter)
        return res.data

    incomes = db.session.query(Income).filter(
        Income.customer_id == customer_id).all()
    incomes_json = model_to_dict(incomes)
    res.update(data=incomes_json)

    return res.data
