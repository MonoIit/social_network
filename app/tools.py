from app.methods import shared_db

menu = [
    {'title': 'Добавить пост', 'url': "feed_bp.add_post"}
]

side_menu = [
    {'title': 'Новости', 'url': "feed_bp.feed"},
    {'title': 'Сообщения', 'url': "messanger_bp.messanger"},
    {'title': 'Друзья', 'url': "friends_bp.friends"}
]


def add_image_and_get_id(image):
    if image and image.filename != '' and allowed_file(image.filename):
        file_data = image.read()
        return shared_db.add_image_and_get_id(name=image.filename, data=file_data)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


def check_friendship(user1_id, user2_id):
    rez = shared_db.find_friendship(user1_id, user2_id)
    if rez and rez['status'] == 'confirmed':
        return True
    else:
        return False


