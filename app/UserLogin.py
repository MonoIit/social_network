from flask_login import UserMixin


class UserLogin(UserMixin):
    def __init__(self, user_data=None):
        if user_data:
            self.id = user_data.get('id')
            self.username = user_data.get('username')
            self.email = user_data.get('email')
            self.password = user_data.get('password')
            self.photo_id = user_data.get('photo_id')

    def create(self, user_data):
        return UserLogin(user_data)

    def get_id(self):
        return str(self.id)

    def get_username(self):
        return self.username

    def get_int_id(self):
        return self.id
