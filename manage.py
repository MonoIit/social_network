from server import create_app, socketio, login_manager

app = create_app()


if __name__ == '__main__':
    login_manager.init_app(app)
    socketio.init_app(app)
    socketio.run(app, host='0.0.0.0', port=5050, allow_unsafe_werkzeug=True)