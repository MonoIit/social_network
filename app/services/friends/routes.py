from flask import request, flash, render_template, session, abort
from flask_login import login_required, current_user

from app.db import friends_db, shared_db
from app.services.friends import friends_bp
from app.tools import tools
from app.tools.tools import menu, side_menu


@friends_bp.route('/friends', methods=['POST', 'GET'])
@login_required
def friends():
    if request.method == 'POST':
        profile_id = request.form['user_id']
        if request.form['action'] == "Отклонить":
            friends_db.delete_friendship(user_id=current_user.get_id(), friend_id=profile_id)
            friends_db.delete_friendship(user_id=profile_id, friend_id=current_user.get_id())
            session['friends'] = shared_db.get_friends_by_id(current_user.get_id())
        elif request.form['action'] == "Принять":
            friends_db.confirm_friendship(user_id=current_user.get_id(), friend_id=profile_id)
            friends_db.confirm_friendship(user_id=profile_id, friend_id=current_user.get_id())
            group = friends_db.find_private_group(current_user.get_id(), profile_id)
            if not group:
                group = shared_db.create_group(name="0", photo_id=None, type="private")
                shared_db.add_user_to_group(current_user.get_id(), group['id'], 'participant')
                shared_db.add_user_to_group(profile_id, group['id'], 'participant')
            session['friends'] = shared_db.get_friends_by_id(current_user.get_id())

    friends = session.get('friends', [])
    return render_template('friends.html', menu=menu, side_menu=side_menu, friends=friends, current_user=current_user)


@friends_bp.route('/add_friend', methods=['POST', 'GET'])
@login_required
def add_friend():
    users = []
    if request.method == "POST":
        user = request.form['username']
        found_users = friends_db.get_similar_users_by_username(user)
        if not found_users:
            flash(f'Пользователь {user} не найден')
        else:
            users = found_users

    return render_template('add_friend.html', menu=menu, side_menu=side_menu, users=users, current_user=current_user)


@friends_bp.route('/profile/<user_id>', methods=["POST", "GET"])
@login_required
def profile(user_id):
    user = shared_db.get_user_by_id(user_id=user_id)
    if not user:
        abort(404)

    if request.method == 'POST':
        if user_id != current_user.get_id():

            if request.form['action'] == "delete":
                friends_db.delete_friendship(user_id=current_user.get_id(), friend_id=user_id)
                friends_db.delete_friendship(user_id=user_id, friend_id=current_user.get_id())
            elif request.form['action'] == "request":
                friends_db.add_friend(from_user_id=current_user.get_id(), to_user_id=user_id)
            elif request.form['action'] == "confirm":
                friends_db.confirm_friendship(user_id=current_user.get_id(), friend_id=user_id)
                friends_db.confirm_friendship(user_id=user_id, friend_id=current_user.get_id())
                group = friends_db.find_private_group(current_user.get_id(), user_id)
                if not group:
                    id = shared_db.create_group(name="0", photo_id=None, type="private")
                    shared_db.add_user_to_group(current_user.get_id(), id, 'paricipant')
                    shared_db.add_user_to_group(user_id, id, 'participant')

            session['friends'] = shared_db.get_friends_by_id(current_user.get_id())
        else:
            profile_id = current_user.get_id()
            image = request.files['image']
            image_id = tools.add_image_and_get_id(image)
            friends_db.update_profile_photo(user_id=profile_id, photo_id=image_id)

    friendship = shared_db.find_friendship(current_user.get_id(), user_id)

    return render_template('profile.html', menu=menu, side_menu=side_menu, user=user, current_user=current_user, friendship=friendship)
