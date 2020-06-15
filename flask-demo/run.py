from app.factory import create_app, create_socketio

app = create_app(config_name="DEVELOPMENT")
app.app_context().push()
socketio = create_socketio(app)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
    # app.run(host="0.0.0.0", port=5000, debug=True)
