from flask import Flask
from flask_socketio import SocketIO
from flask_login import LoginManager
from config import Config
import psycopg2
import base64


def b64encode(value):
    return base64.b64encode(value).decode('utf-8')


socketio = SocketIO()
db = psycopg2.connect(
    host=Config.DB_HOST,
    database=Config.DB_NAME,
    user=Config.DB_USER,
    password=Config.DB_PASSWORD
)

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.jinja_env.filters['b64encode'] = b64encode

    from . import routes
    app.register_blueprint(routes.bp)

    return app

