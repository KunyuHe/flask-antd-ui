from app.factory import create_app, create_socketio

flask_app = create_app(config_name="PRODUCTION")
flask_app.app_context().push()
socketio_app = create_socketio(flask_app)
