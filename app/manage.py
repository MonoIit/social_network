from flask import Flask
from flask_login import LoginManager

import sys
import os

from app.methods import shared_db

# Добавляем путь к корневой директории проекта в PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv()

import base64

from app.db import db
from app.routes import bp
from app.services.auth import auth_bp
from app.services.friends import friends_bp
from app.services.messanger import messanger_bp
from app.services.feed import feed_bp
from app.app_socket import socketio

from app.UserLogin import UserLogin


def b64encode(value):
    return base64.b64encode(value).decode('utf-8')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.jinja_env.filters['b64encode'] = b64encode

app.register_blueprint(bp)
app.register_blueprint(auth_bp)
app.register_blueprint(feed_bp)
app.register_blueprint(friends_bp)
app.register_blueprint(messanger_bp)

login_manager = LoginManager()
login_manager.login_view = 'auth_bp.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    user_data = shared_db.get_user_by_id(user_id)
    if user_data:
        return UserLogin(user_data)
    return None


socketio.init_app(app)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5050, allow_unsafe_werkzeug=True)

