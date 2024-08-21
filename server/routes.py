from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash
from . import db

from .models import User

bp = Blueprint('main', __name__)

menu = [
    {'title': 'Добавить пост', 'url': 'add_post'},
    {'title': 'Войти', 'url': 'login'}
]

side_menu = [
    {'title': 'Новости', 'url': 'feed'},
    {'title': 'Сообщения', 'url': 'messages'},
    {'title': 'Друзья', 'url': 'friend'}
]


@bp.route('/')
def index():
    return render_template('index.html', menu=menu, side_menu=side_menu)


@bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()

        if not existing_user:
            flash('Неверный пользователь или пароль')
        else:
            hashed_password = password
            if hashed_password != existing_user.password:
                flash('Неверный пользователь или пароль')
            else:
                return redirect('')

    return render_template('login.html', menu=menu, side_menu=side_menu)


@bp.route('/add_post', methods=['POST', 'GET'])
def add_post():
    if request.method == 'POST':
        flash('Пост опубликован!')

    return render_template('add_post.html', menu=menu, side_menu=side_menu)


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', menu=menu, side_menu=side_menu)


@bp.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Этот пользователь уже существует')
        else:
            hashed_password = password

            new_user = User(username=username, password=hashed_password, email=email)
            db.session.add(new_user)
            db.session.commit()
            return redirect('')

    return render_template('registration.html', menu=menu, side_menu=side_menu)
