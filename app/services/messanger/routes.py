
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from flask_socketio import join_room, send, SocketIO

from app.db import messanger_db, shared_db
from app.services.messanger import messanger_bp
from app.tools import tools
from app.tools.tools import menu, side_menu


socketio = SocketIO()


@messanger_bp.route('/messanger/chat/<int:group_id>', methods=['GET'])
@login_required
def chat(group_id):
    if not messanger_db.find_user_in_group(group_id, current_user.get_id()):
        return redirect(url_for('messanger_bp.messanger'))
    group = messanger_db.get_group_info(group_id)
    group['role'] = messanger_db.get_user_privilege_in_group(group_id, current_user.get_id())
    if not group:
        return redirect(url_for('messanger_bp.messanger'))
    if group['type'] == 'private':
        user1, user2 = messanger_db.get_group_participants(group_id)
        if not tools.check_friendship(user1['user_id'], user2['user_id']):
            return redirect(url_for('messanger_bp.messanger'))
    messages = messanger_db.get_ten_last_messages(group_id)
    return render_template('chat.html', menu=menu, side_menu=side_menu, current_user=current_user, group=group,
                           messages=messages)


@messanger_bp.route('/messanger', methods=['GET'])
@login_required
def messanger():
    chats = messanger_db.get_user_groups(current_user.get_id())
    return render_template('messanger.html', menu=menu, side_menu=side_menu, current_user=current_user, chats=chats)


@messanger_bp.route('/group/construct', methods=['GET', 'POST'])
@login_required
def create_group():
    if request.method == 'POST':
        name = request.form['name']
        image = request.files['image']
        try:
            image_id = tools.add_image_and_get_id(image)
            group = shared_db.create_group(name, image_id, 'public')
            shared_db.add_user_to_group(current_user.get_id(), group['id'], 'admin')
            return redirect(url_for('messanger_bp.chat', group_id=group['id']))
        except Exception as e:
            flash('Возникла ошибка при создании группы')
            print(f"[!] Error: {e}")
            return redirect(url_for('messanger_bp.create_group'))

    return render_template('create_chat_form.html', menu=menu, side_menu=side_menu, current_user=current_user)


@messanger_bp.route('/group/edit/<int:group_id>', methods=['GET', 'POST'])
@login_required
def edit_group(group_id):
    group = messanger_db.get_group_info(group_id)
    group['role'] = messanger_db.get_user_privilege_in_group(group_id, current_user.get_id())
    if group['role'] != 'admin':
        return redirect(url_for('feed_bp.feed'))
    if request.method == 'POST':
        name = request.form.get('name')
        if not name:
            flash('Введите название группы')
        else:
            image = request.files['image']
            image_id = tools.add_image_and_get_id(image) if image else group['photo_id']

            try:
                messanger_db.update_group(group_id, name, image_id)
                return redirect(url_for('messanger_bp.messanger'))
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

    messanger_db.add_message(group_id, current_user.get_id(), msg)
    # Отправляем сообщение обратно в комнату
    send(f"{user}: {msg}", to=group_id)
