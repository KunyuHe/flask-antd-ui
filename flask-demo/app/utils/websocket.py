# from ..factory import socketio


# class Websocket:
#     __socketio__ = None
#
#     @classmethod
#     def set_socketio(cls, socket_io):
#         cls.__socketio__ = socket_io
#         socketio = socket_io
#
#     @classmethod
#     def get_socketio(cls):
#         return cls.__socketio__
#
#     @classmethod
#     def send_trade(self, trade):
#         socketio = Websocket.get_socketio()
#         # socketio.emit('hi', {"hello": 1}, namespace="/trade")
#         socketio.emit("hi", {'data': "hello"}, namespace='/trade', broadcast=True)

#
# @socketio.on('message')
# def handle_message(message):
#     print('received message: ' + message)
#
#
# @socketio.on('json')
# def handle_json(json):
#     print('received json: ' + str(json))


# @socketio.on('my event')
from app.factory import socketio



