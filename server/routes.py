from flask import Blueprint, render_template, request, flash, redirect, session, abort, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import send, join_room
from flask_login import login_user, logout_user, login_required, current_user
from .UserLogin import UserLogin
from . import db, socketio, login_manager
from .PostgresDB import PostgresDB


bp = Blueprint('main', __name__)

menu = [
    {'title': 'Добавить пост', 'url': "add_post"}
]

side_menu = [
    {'title': 'Новости', 'url': "feed"},
    {'title': 'Сообщения', 'url': "messanger"},
    {'title': 'Друзья', 'url': "friends"}
]


dbase = PostgresDB(db)
login_manager.login_view = 'main.login'


@login_manager.user_loader
def load_user(user_id):
    user_data = dbase.get_user_by_id(user_id)
    if user_data:
        return UserLogin(user_data)
    return None


@bp.route('/feed')
@login_required
def feed():
    posts = dbase.get_posts()
    return render_template('index.html', menu=menu, side_menu=side_menu, current_user=current_user, posts=posts)


@bp.route('/')
@login_required
def index():
    return redirect('feed')


@bp.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('logout')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = dbase.get_user_by_username(username)

        if existing_user and check_password_hash(existing_user['password'], password):
            userlogin = UserLogin().create(existing_user)
            login_user(userlogin)
            session['friends'] = dbase.get_friend_by_id(current_user.id)
            return redirect('feed')
        else:
            flash('Неверный пользователь или пароль')

    return render_template('login.html', menu=menu, side_menu=side_menu, current_user=current_user)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect('login')


@bp.route('/add_post', methods=['POST', 'GET'])
@login_required
def add_post():
    if request.method == 'POST':
        author_id = request.form['user_id']
        message = request.form['news']
        image = request.files['image']
        if not message and not image:
            flash('Напишите хоть что-нибудь или загрузите изображение')
        else:
            image = request.files['image']
            image_id = add_image_and_get_id(image)

            dbase.create_post(author_id, message, image_id)
            flash('Пост опубликован!')

    return render_template('add_post.html', menu=menu, side_menu=side_menu, current_user=current_user)


@bp.route('/cccc/<user_id>', methods=['GET'])
@login_required
def check_friendship(user_id):
    rez = dbase.find_friendship(current_user.get_id(), user_id)
    if rez and rez['status'] == 'confirmed':
        group = dbase.find_private_group(current_user.get_id(), user_id)
        if not group:
            group = dbase.create_personal_group(current_user.get_id(), user_id)
        return redirect(url_for('main.chat', group_id=group['group_id'], type='private'))
    else:
        return redirect(url_for('main.messanger'))


@bp.route('/messanger/chat', methods=['GET', 'POST'])
@login_required
def chat():
    id = request.args.get('group_id')
    type = request.args.get('type')
    if type == 'public':
        group = dbase.get_public_group_info_by_user(current_user.get_id(), id)
        if not group:
            return redirect(url_for('main.messanger'))
        messages = dbase.get_ten_last_messages(id)
    elif type == 'private':
        group = dbase.get_private_group_by_id(id)
        if not group or not current_user.get_int_id() in (group['user1_id'], group['user2_id']):
            return redirect(url_for('main.messanger'))
        messages = dbase.get_ten_last_messages(id)
    else:
        return redirect(url_for('main.messanger'))
    return render_template('chat.html', menu=menu, side_menu=side_menu, current_user=current_user, group=group,
                           messages=messages)


@bp.route('/messanger', methods=['POST', 'GET'])
@login_required
def messanger():
    if request.method == 'POST':
        ...

    chats = dbase.get_user_personal_groups(current_user.get_id()) + dbase.get_user_public_groups(current_user.get_id())
    return render_template('messanger.html', menu=menu, side_menu=side_menu, current_user=current_user, chats=chats)


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', menu=menu, side_menu=side_menu, current_user=current_user)


@bp.route('/registration', methods=['POST', 'GET'])
def registration():
    if current_user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        existing_user = dbase.get_user_by_username(username)
        if existing_user:
            flash('Этот пользователь уже существует')
        else:
            image = request.files['image']
            image_id = add_image_and_get_id(image)

            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

            dbase.create_user(username=username, password=hashed_password, email=email, photo_id=image_id)
            return redirect('feed')

    return render_template('registration.html', menu=menu, side_menu=side_menu, current_user=current_user)


@bp.route('/friends', methods=['POST', 'GET'])
@login_required
def friends():
    if request.method == 'POST':
        profile_id = request.form['user_id']
        if request.form['action'] == "Отклонить":
            dbase.delete_friendship(user_id=current_user.get_id(), friend_id=profile_id)
            dbase.delete_friendship(user_id=profile_id, friend_id=current_user.get_id())
            session['friends'] = dbase.get_friend_by_id(current_user.get_id())
        elif request.form['action'] == "Принять":
            dbase.confirm_friendship(user_id=current_user.get_id(), friend_id=profile_id)
            dbase.confirm_friendship(user_id=profile_id, friend_id=current_user.get_id())
            session['friends'] = dbase.get_friend_by_id(current_user.get_id())

    friends = session.get('friends', [])
    return render_template('friends.html', menu=menu, side_menu=side_menu, friends=friends, current_user=current_user)


@bp.route('/add_friend', methods=['POST', 'GET'])
@login_required
def add_friend():
    users = []
    if request.method == "POST":
        user = request.form['username']
        found_users = dbase.get_similar_users_by_username(user)
        if not found_users:
            flash(f'Пользователь {user} не найден')
        else:
            users = found_users

    return render_template('add_friend.html', menu=menu, side_menu=side_menu, users=users, current_user=current_user)


@bp.route('/profile/<user_id>', methods=["POST", "GET"])
@login_required
def profile(user_id):
    user = dbase.get_user_by_id(user_id=user_id)
    if not user:
        abort(404)

    if request.method == 'POST':
        if user_id != current_user.get_id():

            if request.form['action'] == "delete":
                dbase.delete_friendship(user_id=current_user.get_id(), friend_id=user_id)
                dbase.delete_friendship(user_id=user_id, friend_id=current_user.get_id())
            elif request.form['action'] == "request":
                dbase.add_friend(from_user_id=current_user.get_id(), to_user_id=user_id)
            elif request.form['action'] == "confirm":
                dbase.confirm_friendship(user_id=current_user.get_id(), friend_id=user_id)
                dbase.confirm_friendship(user_id=user_id, friend_id=current_user.get_id())
            session['friends'] = dbase.get_friend_by_id(current_user.get_id())
        else:
            profile_id = current_user.get_id()
            image = request.files['image']
            image_id = add_image_and_get_id(image)
            dbase.update_profile_photo(user_id=profile_id, photo_id=image_id)

    friendship = dbase.find_friendship(current_user.get_id(), user_id)

    return render_template('profile.html', menu=menu, side_menu=side_menu, user=user, current_user=current_user, friendship=friendship)


@bp.route('/group/construct', methods=['GET', 'POST'])
@login_required
def create_group():
    if request.method == 'POST':
        name = request.form['name']
        image = request.files['image']
        try:
            image_id = add_image_and_get_id(image)
            group = dbase.create_public_group(name, image_id)
            dbase.add_user_to_group(current_user.get_id(), group['id'], 'admin')
            return redirect(url_for('main.chat', group_id=group['id']))
        except Exception as e:
            flash('Возникла ошибка при создании группы')
            print(f"[!] Error: {e}")
            return redirect(url_for('main.create_group'))

    return render_template('create_chat_form.html', menu=menu, side_menu=side_menu, current_user=current_user)


@bp.route('/group/edit/<int:group_id>', methods=['GET', 'POST'])
@login_required
def edit_group(group_id):
    group = dbase.get_public_group(group_id)

    if request.method == 'POST':
        name = request.form.get('name')
        if not name:
            flash('Введите название группы')
        else:
            image = request.files['image']
            image_id = add_image_and_get_id(image) if image else group['photo_id']

            try:
                dbase.update_public_group(group_id, name, image_id)
                return redirect(url_for('main.messanger'))
            except Exception as e:
                flash("Произошла ошибка")
                print(f"[!] Error: {e}")

    return render_template('edit_chat_form.html', menu=menu, side_menu=side_menu, current_user=current_user, group=group)



@socketio.on('connect')
def handle_connect():
    print("User connected")


@socketio.on('join')
def on_join(data):
    username = data['username']
    group_id = data['group_id']
    join_room(group_id)



@socketio.on('message')
def handle_message(data):
    user = data['user']
    group_id = data['group_id']
    msg = data['msg']

    dbase.add_message(group_id, current_user.get_id(), msg)
    # Отправляем сообщение обратно в комнату
    send(f"{user}: {msg}", to=group_id)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


def add_image_and_get_id(image):
    if image and image.filename != '' and allowed_file(image.filename):
        file_data = image.read()
        return dbase.add_image_and_get_id(name=image.filename, data=file_data)['id']

