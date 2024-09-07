from app import create_app
from app.services.messanger.routes import socketio

app = create_app()


if __name__ == '__main__':
    socketio.init_app(app)
    socketio.run(app, host='0.0.0.0', port=5050, allow_unsafe_werkzeug=True)