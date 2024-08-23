import psycopg2 as p
from psycopg2.extras import RealDictCursor


class PostgresDB:
    def __init__(self, db):
        self.__db = db
        self.__cursor = db.cursor(cursor_factory=RealDictCursor)

    def get_user_by_id(self, user_id):
        sql = f"""SELECT * FROM public."User" WHERE id = {user_id}"""
        try:
            self.__cursor.execute(sql)
            res = self.__cursor.fetchone()
            if res:
                return res
        except Exception as e:
            print(f"[!] Error: {e}")
        return []

    def get_user_by_username(self, username):
        sql = f"""SELECT * FROM public."User" WHERE username = '{username}' LIMIT 1"""
        try:
            self.__cursor.execute(sql)
            res = self.__cursor.fetchone()
            if res:
                return res
        except Exception as e:
            print(f"[!] Error: {e}")
        return []

    def get_similar_users_by_username(self, username):
        sql = f"""SELECT * FROM public."User" WHERE username ILIKE '%{username}%'"""
        try:
            self.__cursor.execute(sql)
            res = self.__cursor.fetchall()
            if res:
                return res
        except Exception as e:
            print(f"[!] Error: {e}")
        return []

    def create_user(self, username, password, email):
        sql = f"""
        INSERT INTO public."User" 
            username,
            email,
            password
        VALUES 
            '{username}',
            '{email}',
            '{password}');
        """
        self.__cursor.execute(sql)
        self.__db.commit()

    def get_friend_by_id(self, from_user_id):
        sql = f"""
        SELECT 
            u.id,
            u.username,
            f.status
        FROM 
            public."User_friends" f
        JOIN 
            public."User" u 
            ON (f.user_id = {from_user_id} and f.friend_id = u.id);
        """
        try:
            self.__cursor.execute(sql)
            res = self.__cursor.fetchall()
            if res:
                return res
        except Exception as e:
            print(f"[!] Error: {e}")
        return []

    def add_friend(self, from_user_id, to_user_id):
        sql = f"""
        INSERT INTO public."User_friends" VALUES ({from_user_id}, {to_user_id}, 'sent');
        INSERT INTO public."User_friends" VALUES ({to_user_id}, {from_user_id}, 'received');
        """
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
        except Exception as e:
            print(f"[!] Error: {e}")
            self.__db.rollback()


    def find_friendship(self, from_user_id, to_user_id):
        sql = f"""
        SELECT status FROM public."User_friends" WHERE user_id = {from_user_id} AND friend_id = {to_user_id};
        """
        try:
            self.__cursor.execute(sql)
            res = self.__cursor.fetchone()
            if res:
                return res
        except Exception as e:
            print(f"[!] Error: {e}")
        return []

    def confirm_friendship(self, user_id, friend_id):
        sql = f"""
        UPDATE public."User_friends"
        SET status = 'confirm'
        WHERE 
            (user_id = {user_id} AND friend_id = {friend_id});
        """
        self.__cursor.execute(sql)
        self.__db.commit()

    def delete_friendship(self, user_id, friend_id):
        sql = f"""
        DELETE FROM public."User_friends"
        WHERE 
            (user_id = {user_id} AND friend_id = {friend_id});
        """
        self.__cursor.execute(sql)
        self.__db.commit()

