from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import send
from flask_login import login_user, logout_user, login_required, current_user
from .UserLogin import UserLogin
from . import db, socketio, login_manager
from .PostgresDB import PostgresDB


bp = Blueprint('main', __name__)

menu = [
    {'title': 'Добавить пост', 'url': 'add_post'},
    {'title': 'Войти', 'url': 'login'}
]

side_menu = [
    {'title': 'Новости', 'url': 'feed'},
    {'title': 'Сообщения', 'url': 'messanger'},
    {'title': 'Друзья', 'url': 'friends'}
]

dbase = PostgresDB(db)
login_manager.login_view = 'main.login'

@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, dbase)


@bp.route('/feed')
@login_required
def feed():
    return render_template('index.html', menu=menu, side_menu=side_menu)


@bp.route('/')
def index():
    return redirect('feed')


@bp.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('logout')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = dbase.get_user_by_username(username, registration=True)[0]

        if existing_user and check_password_hash(existing_user['password'], password):
            userlogin = UserLogin().create(existing_user)
            login_user(userlogin)
            return redirect('feed')
        else:
            flash('Неверный пользователь или пароль')

    return render_template('login.html', menu=menu, side_menu=side_menu)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('login')


@bp.route('/add_post', methods=['POST', 'GET'])
@login_required
def add_post():
    if request.method == 'POST':
        flash('Пост опубликован!')

    return render_template('add_post.html', menu=menu, side_menu=side_menu)


@bp.route('/messanger', methods=['POST', 'GET'])
@login_required
def messanger():
    if request.method == 'POST':
        ...

    return render_template('messanger.html', menu=menu, side_menu=side_menu)


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', menu=menu, side_menu=side_menu)


@bp.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        existing_user = dbase.get_user_by_username(username, registration=True)
        if existing_user:
            flash('Этот пользователь уже существует')
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

            dbase.create_user(username=username, password=hashed_password, email=email)
            return redirect('')

    return render_template('registration.html', menu=menu, side_menu=side_menu)


@bp.route('/friends', methods=['POST', 'GET'])
@login_required
def friends():
    friends = dbase.get_user_by_username('')
    return render_template('friends.html', menu=menu, side_menu=side_menu, friends=friends)


@bp.route('/add_friend', methods=['POST', 'GET'])
@login_required
def add_friend():
    users = []
    if request.method == "POST":
        user = request.form['username']
        found_users = dbase.get_user_by_username(user)
        if not found_users:
            flash(f'Пользователь {user} не найден')
        else:
            users = found_users

    return render_template('add_friend.html', menu=menu, side_menu=side_menu, users=users)


@bp.route('/profile/<user_id>')
@login_required
def profile(user_id):
    user = dbase.get_user_by_id(user_id=user_id)
    if not user:
        abort(404)
    return render_template('profile.html', menu=menu, side_menu=side_menu, user=user[0])

@socketio.on('message')
def handle_message(msg):
    send(msg, broadcast=True)

