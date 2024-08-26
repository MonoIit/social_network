import psycopg2
import psycopg2 as p
from psycopg2.extras import RealDictCursor

schema = 'sn.'


class PostgresDB:
    def __init__(self, db):
        self.__db = db
        self.__cursor = db.cursor(cursor_factory=RealDictCursor)

    def get_user_by_id(self, user_id):
        sql = f"""
        SELECT 
            u.id as id,
            username,
            email,
            data as photo
        FROM {schema}"Users" u
        LEFT JOIN {schema}"Photos" p 
            ON photo_id = p.id
        WHERE u.id = %s;
        """
        try:
            self.__cursor.execute(sql, (user_id,))
            res = self.__cursor.fetchone()
            if res:
                return res
        except Exception as e:
            print(f"[!] Error: {e}")
        return []

    def get_user_by_username(self, username):
        sql = f"""
        SELECT 
            u.id as id,
            username,
            email,
            password,
            p.data as photo
        FROM {schema}"Users" u
        LEFT JOIN {schema}"Photos" p ON photo_id = p.id
        WHERE username = %s
        LIMIT 1;
        """
        try:
            self.__cursor.execute(sql, (username,))
            res = self.__cursor.fetchone()
            if res:
                return res
        except Exception as e:
            print(f"[!] Error: {e}")
        return []

    def get_similar_users_by_username(self, username):
        sql = f"""
        SELECT * FROM {schema}"Users" 
        WHERE username ILIKE '%{username}%';
        """
        try:
            self.__cursor.execute(sql)
            res = self.__cursor.fetchall()
            if res:
                return res
        except Exception as e:
            print(f"[!] Error: {e}")
        return []

    def create_user(self, username, email, password, photo_id):
        sql = f"""
        INSERT INTO {schema}"Users" 
            (username,
            email,
            password,
            photo_id)
        VALUES 
            (%s, %s, %s, %s);
        """
        try:
            self.__cursor.execute(sql, (username, email, password, photo_id))
            self.__db.commit()
        except Exception as e:
            print(f"[!] Error: {e}")
            self.__db.rollback()

    def get_friend_by_id(self, from_user_id):
        sql = f"""
        SELECT 
            u.id,
            u.username,
            f.status
        FROM 
            {schema}"Friends" f
        JOIN 
            {schema}"Users" u 
            ON (f.user_id = %s and f.friend_id = u.id);
        """
        try:
            self.__cursor.execute(sql, (from_user_id,))
            res = self.__cursor.fetchall()
            if res:
                return res
        except Exception as e:
            print(f"[!] Error: {e}")
        return []

    def add_friend(self, from_user_id, to_user_id):
        sql = f"""
        INSERT INTO {schema}"Friends" VALUES (%s, %s, 'sent');
        INSERT INTO {schema}"Friends" VALUES (%s, %s, 'received');
        """
        try:
            self.__cursor.execute(sql, (from_user_id, to_user_id, to_user_id, from_user_id))
            self.__db.commit()
        except Exception as e:
            print(f"[!] Error: {e}")
            self.__db.rollback()

    def find_friendship(self, from_user_id, to_user_id):
        sql = f"""
        SELECT status FROM {schema}"Friends" 
        WHERE 
            user_id = %s AND friend_id = %s;
        """
        try:
            self.__cursor.execute(sql, (from_user_id, to_user_id))
            res = self.__cursor.fetchone()
            if res:
                return res
        except Exception as e:
            print(f"[!] Error: {e}")
        return []

    def confirm_friendship(self, user_id, friend_id):
        sql = f"""
        UPDATE {schema}"Friends"
        SET status = 'confirmed'
        WHERE 
            user_id = %s AND friend_id = %s;
        """
        try:
            self.__cursor.execute(sql, (user_id, friend_id))
            self.__db.commit()
        except Exception as e:
            print(f"[!] Error: {e}")
            self.__db.rollback()


    def delete_friendship(self, user_id, friend_id):
        sql = f"""
        DELETE FROM {schema}"Friends"
        WHERE 
            user_id = %s AND friend_id = %s;
        """
        try:
            self.__cursor.execute(sql, (user_id, friend_id))
            self.__db.commit()
        except Exception as e:
            print(f"[!] Error: {e}")
            self.__db.rollback()

    def create_post(self, author_id, message, image_id):
        sql = f"""
        INSERT INTO {schema}"Posts"
            (author_id,
            message)
        VALUES
            (%s, %s)
        RETURNING id;
        """
        try:
            self.__cursor.execute(sql, (author_id, message))
            post = self.__cursor.fetchone()
            if post:
                post_id = post['id']
                if image_id:
                    self.__connect_image_to_post(post_id=post_id, image_id=image_id)
                self.__db.commit()
        except Exception as e:
            print(f"[!] Error: {e}")
            self.__db.rollback()

    def get_posts(self):
        sql = f"""
        SELECT 
            p.id AS post_id,
            u.id AS author_id,
            u.username AS author_username,
            p.message AS message,
            p1.data AS author_photo,
            p2.data AS post_photos
        FROM 
            {schema}"Photos_Posts" pp
        LEFT JOIN 
            {schema}"Posts" p ON pp."Posts_id"= p.id
        LEFT JOIN 
            {schema}"Users" u ON p.author_id = u.id
        LEFT JOIN 
            {schema}"Photos" p1 ON u.id = u.photo_id
        LEFT JOIN 
            {schema}"Photos" p2 ON pp."Photos_id" = p2.id
        ORDER BY 
            p.id
        LIMIT 10;
        """
        try:
            self.__cursor.execute(sql)
            res = self.__cursor.fetchall()
            if res:
                return res
        except Exception as e:
            print(f"[!] Error: {e}")
            self.__db.rollback()
        return []

    def add_image_and_get_id(self, name, data):
        sql = f"""
        INSERT INTO {schema}"Photos" 
            (filename, 
            data) 
        VALUES 
            (%s, %s) 
        RETURNING id;
        """
        try:
            self.__cursor.execute(sql, (name, psycopg2.Binary(data)))
            image_id = self.__cursor.fetchone()
            return image_id
        except Exception as e:
            print(f"[!] Error: {e}")
            self.__db.rollback()
            return 0

    def update_profile_photo(self, user_id, photo_id):
        sql = f"""
        UPDATE {schema}"Users"
        SET photo_id = %s
        WHERE id = %s
        """
        try:
            self.__cursor.execute(sql, (photo_id, user_id))
            self.__db.commit()
        except Exception as e:
            print(f"[!] Error: {e}")
            self.__db.rollback()

    def __connect_image_to_post(self, post_id, image_id):
        sql = f"""
        INSERT INTO {schema}"Photos_Posts"
            ("Photos_id",
            "Posts_id")
        VALUES
            (%s, %s);
        """
        try:
            self.__cursor.execute(sql, (image_id, post_id))
            self.__db.commit()
        except Exception as e:
            print(f"[!] Error: {e}")
            self.__db.rollback()

