from flask import Flask
from flask_login import LoginManager
from config import Config
import base64

from .routes import bp
from .services.auth import auth_bp
from .services.friends import friends_bp
from .services.messanger import messanger_bp
from .services.feed import feed_bp

from app.UserLogin import UserLogin
from app.db import users_db, shared_db


def b64encode(value):
    return base64.b64encode(value).decode('utf-8')


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
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

    return app

