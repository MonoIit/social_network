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
            res = self.__cursor.fetchall()
            if res:
                return res
        except Exception as e:
            print(f"[!] Error: {e}")
        return []

    def get_user_by_username(self, username, registration=False):
        if registration:
            sql = f"""SELECT * FROM public."User" WHERE username = '{username}' LIMIT 1"""
        else:
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
        sql = f"""INSERT INTO public."User" (username, email, password) VALUES ('{username}', '{email}', '{password}');"""
        self.__cursor.execute(sql)
        self.__db.commit()







