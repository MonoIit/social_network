from flask import redirect, request, session, flash, render_template, url_for
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.UserLogin import UserLogin
from app.services.auth import auth_bp
from app.methods import users_db
import app.tools as tools
from app.tools import menu, side_menu



@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth_bp.logout'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = users_db.get_user_by_username(username)

        if existing_user and check_password_hash(existing_user['password'], password):
            userlogin = UserLogin().create(existing_user)
            login_user(userlogin)
            return redirect(url_for('feed_bp.feed'))
        else:
            flash('Неверный пользователь или пароль')

    return render_template('login.html', menu=menu, side_menu=side_menu, current_user=current_user)


@auth_bp.route('/registration', methods=['POST', 'GET'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('feed_bp.feed'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if not username or not password or not email:
            flash('Заполните все данные!')
        else:
            existing_user = users_db.get_user_by_username(username)
            if existing_user:
                flash('Этот пользователь уже существует')
            else:
                image = request.files['image']
                image_id = tools.add_image_and_get_id(image)

                hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

                users_db.create_user(username=username, password=hashed_password, email=email, photo_id=image_id)
            return redirect(url_for('feed_bp.feed'))

    return render_template('registration.html', menu=menu, side_menu=side_menu, current_user=current_user)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('auth_bp.login'))



