import logging
import sys
from flask import Blueprint
from flask import request

from app.models.model import Customer, Trade
from app.utils.core import db
from app.utils.response import ResponseCode, ResMsg
from app.utils.util import route

sys.path.append("..")

from flask_socketio import Namespace, emit, send
from app.utils.util import model_to_dict

bp = Blueprint("api_trade", __name__, url_prefix='/trade')
logger = logging.getLogger(__name__)


@route(bp, '/add', methods=["POST"])
def add_trade():
    res = ResMsg()
    obj = request.get_json(force=True)

    customer_name = obj.get("customer_name")
    customer = db.session.query(Customer).filter(
        Customer.name == customer_name).first()
    if not obj or not customer_name or not customer:
        res.update(ResponseCode.InvalidParameter)
        return res.data

    trade = Trade()
    trade.customer_id = customer.id
    trade.feedback = 0
    db.session.add(trade)
    db.session.commit()
    res.update(data=trade.customer_id)

    return res.data
