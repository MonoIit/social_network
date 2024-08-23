class UserLogin():
    def fromDB(self, user_id, db):
        self.__user = db.get_user_by_id(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user['id'])

    def get_username(self):
        return str(self.__user['username'])
