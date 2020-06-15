import datetime
import logging
from flask_socketio import Namespace, emit
from threading import Lock

from app.models.model import Trade
from app.utils.core import db
from app.utils.util import model_to_dict

logger = logging.getLogger(__name__)

thread = None
thread_lock = Lock()
connections = 0

NS_DATA_PUSH = "flask"


def background_thread():
    count = 0
    while True:
        TradeNamespace.get_socketio().sleep(5)
        count += 1
        with db.app.app_context():
            try:
                trades = db.session.query(Trade).filter(
                    Trade.feedback == 0).all()
                if not trades:
                    continue
                # 向前端发送需求
                trades_json = model_to_dict(trades)
                TradeNamespace.get_socketio().emit('hi',
                                                   trades_json,
                                                   namespace="/flask")
                for trade in trades:
                    trade.feedback = 1
                    db.session.add(trade)
                db.session.commit()

            except Exception as ex:
                logger.error(ex)


class TradeNamespace(Namespace):
    __send_time__ = None
    __socketio__ = None

    @classmethod
    def set_send_time(cls, time):
        cls.__send_time__ = time

    @classmethod
    def get_send_time(cls, time):
        return cls.__send_time__

    @classmethod
    def set_socketio(cls, socketio):
        cls.__socketio__ = socketio

    @classmethod
    def get_socketio(cls):
        return cls.__socketio__

    def on_connect(self):
        global thread, thread_lock, connections
        with thread_lock:
            connections += 1
            logger.info('Connection +1')
            if (thread is None) or (not thread.is_alive()):
                thread = TradeNamespace.get_socketio().start_background_task(
                    background_thread)

    def on_disconnect(self):
        global thread, thread_lock, connections
        with thread_lock:
            if connections >= 1:
                connections -= 1
            logger.info('Connection -1')

    def on_reconnect(self):
        global thread
        with thread_lock:
            if connections >= 0:
                if not thread.is_alive():
                    thread = TradeNamespace.get_socketio().start_background_task(
                        background_thread())

    def on_my_event(self, data):
        emit('hi', data)
