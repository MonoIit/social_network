from flask import render_template, request, flash
from flask_login import login_required, current_user

from app.db import feed_db, shared_db
from app.services.feed import feed_bp
from app.tools.tools import menu, side_menu


@feed_bp.route('/feed')
@login_required
def feed():
    posts = feed_db.get_posts()
    return render_template('index.html', menu=menu, side_menu=side_menu, current_user=current_user, posts=posts)


@feed_bp.route('/add_post', methods=['POST', 'GET'])
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
            image_id = shared_db.add_image_and_get_id(image)

            feed_db.create_post(author_id, message, image_id)
            flash('Пост опубликован!')

    return render_template('add_post.html', menu=menu, side_menu=side_menu, current_user=current_user)
