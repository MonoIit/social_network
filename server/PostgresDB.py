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
            photo_id,
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
        WITH UserFriends AS (
            -- Находим всех друзей пользователя
            SELECT 
                f.friend_id,
                f.status,
                u.username,
                p.data as photo
            FROM sn."Friends" f
            JOIN sn."Users" u ON f.friend_id = u.id
            LEFT JOIN sn."Photos" p ON u.photo_id = p.id
            WHERE (f.user_id = %s)
        ),
        PrivateGroups AS (
            -- Находим группы типа 'private', в которых участвуют друзья пользователя
            SELECT 
                p1.user_id,
                g.id AS group_id
            FROM sn."Groups" g
            JOIN sn."Participants" p1 ON g.id = p1.group_id  -- Проверяем участие друга
            JOIN sn."Participants" p2 ON g.id = p2.group_id  -- Проверяем участие пользователя
            WHERE g.type = 'private' 
              AND p1.user_id IN (SELECT friend_id FROM UserFriends)  -- Друг в группе
              AND p2.user_id = %s  -- Пользователь в группе
        )
        SELECT 
            uf.friend_id as id,
            uf.username,
            uf.status,
            pg.group_id
        FROM UserFriends uf
        LEFT JOIN PrivateGroups pg ON pg.user_id = uf.friend_id;
        """
        try:
            self.__cursor.execute(sql, (from_user_id, from_user_id))
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
            p1.data AS post_photo,
            p2.data AS user_photo
        FROM 
            {schema}"Posts" p 
        LEFT JOIN 
            {schema}"Photos_Posts" pp ON pp."Posts_id"= p.id
        JOIN 
            {schema}"Users" u ON p.author_id = u.id
        LEFT JOIN
            {schema}"Photos" p1 ON pp."Photos_id" = p1.id
        LEFT JOIN
            {schema}"Photos" p2 ON u.photo_id = p2.id
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
            self.__db.commit()
            return image_id['id']
        except Exception as e:
            print(f"[!] Error: {e}")
            self.__db.rollback()


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

    def get_private_group_by_id(self, group_id):
        sql = f"""
        SELECT
            group_id,
            user_id,
            created_at,
            type 
        FROM {schema}"Groups" WHERE group_id = %s;
        """
        self.__cursor.execute(sql, (group_id,))
        rez = self.__cursor.fetchone()
        return rez


    def create_group(self, name, photo_id, type):
        sql = f"""
        INSERT INTO {schema}"Groups"
            (name,
            photo_id,
            type)
        VALUES (%s, %s, %s)
        RETURNING id;
        """
        try:
            self.__cursor.execute(sql, (name, photo_id, type))
            group_id = self.__cursor.fetchone()
            return group_id
        except Exception as e:
            print(f"[!] Error: {e}")
            self.__db.rollback()
        return -1

    def get_user_groups(self, user_id):
        sql = f"""
        WITH PublicGroups AS (
            -- Находим все публичные группы, в которых участвует заданный пользователь
            SELECT 
                g.id AS id,
                g.name AS name,
                g.type AS type,
                ph.data AS photo,
                p.user_id AS user_id  -- Пользователь, участвующий в группе
            FROM sn."Groups" g
            JOIN sn."Participants" p ON g.id = p.group_id AND g.type = 'public'
            LEFT JOIN sn."Photos" ph ON g.photo_id = ph.id
            WHERE p.user_id = %s
        ),
        PrivateGroups AS (
            -- Находим все приватные группы, в которых участвует заданный пользователь
            SELECT
                p1.group_id as id,
                u.username as name,
                g.type as type,
                ph.data as photo,
                p1.user_id as user_id
            FROM sn."Participants" p1
            JOIN sn."Participants" p2 ON p1.group_id = p2.group_id AND p1.user_id = %s AND p2.user_id <> %s
            JOIN sn."Groups" g ON p1.group_id = g.id AND g.type = 'private'
            JOIN sn."Users" u ON p2.user_id = u.id
            LEFT JOIN sn."Photos" ph ON u.photo_id = ph.id
        )
        SELECT * FROM PrivateGroups
        UNION ALL
        SELECT * FROM PublicGroups;
        """
        self.__cursor.execute(sql, (user_id, user_id, user_id))
        rez = self.__cursor.fetchall()
        return rez

    def find_private_group(self, user1_id, user2_id):
        sql = f"""
        SELECT
            p1.group_id as id,
            g.type
        FROM {schema}"Participants" p1
        JOIN {schema}"Participants" p2
        ON
            (p1.user_id = %s AND p2.user_id = %s)
        JOIN {schema}"Groups" g
        ON
            p1.group_id = g.id;
        """
        self.__cursor.execute(sql, (user1_id, user2_id))
        rez = self.__cursor.fetchone()
        return rez

    def update_group(self, group_id, name, photo_id):
        sql = f"""
        UPDATE 
            {schema}"Groups"
        SET 
            name = %s, photo_id = %s
        WHERE
            id = %s  
        """
        try:
            self.__cursor.execute(sql, (name, photo_id, group_id))
            self.__db.commit()
        except Exception as e:
            print(f"[!] Error: {e}")
            self.__db.rollback()

    def add_user_to_group(self, user_id, group_id, role):
        sql = f"""
        INSERT INTO {schema}"Participants"
            (user_id,
            group_id,
            role)
        VALUES (%s, %s, %s);
        """
        try:
            self.__cursor.execute(sql, (user_id, group_id, role))
            self.__db.commit()
        except Exception as e:
            print(f"[!] Error: {e}")
            self.__db.rollback()

    def get_group_info(self, group_id):
        sql = f"""
        SELECT
            pg.id as id,
            pg.name,
            pg.type,
            pg.photo_id,
            p.data as photo
        FROM
            {schema}"Groups" pg
        LEFT JOIN
            {schema}"Photos" p
        ON
            pg.photo_id = p.id
        WHERE
            pg.id = %s; 
        """
        self.__cursor.execute(sql, (group_id,))
        rez = self.__cursor.fetchone()
        return rez

    def add_message(self, group_id, user_id, content):
        sql = f"""
        INSERT INTO {schema}"Messages"
            (user_id,
            group_id,
            content)
        VALUES (%s, %s, %s)
        """
        try:
            self.__cursor.execute(sql, (user_id, group_id, content))
            self.__db.commit()
        except Exception as e:
            print(f"[!] Error: {e}")
            self.__db.rollback()

    def get_ten_last_messages(self, group_id):
        sql = f"""
        SELECT 
            u.username,
            m.content 
        FROM {schema}"Messages" m
        JOIN {schema}"Users" u
        ON m.user_id = u.id AND m.group_id = %s
        ORDER BY 
            created_at DESC
        LIMIT 10;
        """
        self.__cursor.execute(sql, (group_id,))
        rez = self.__cursor.fetchall()[::-1]
        return rez

    def get_group_participants(self, group_id):
        sql = f"""
        SELECT
            user_id
        FROM {schema}"Participants"
        WHERE
            group_id = %s;
        """
        self.__cursor.execute(sql, (group_id,))
        rez = self.__cursor.fetchall()
        return rez

    def find_user_in_group(self, group_id, user_id):
        sql = f"""
        SELECT * FROM {schema}"Participants" WHERE group_id = %s AND user_id = %s;
        """
        self.__cursor.execute(sql, (group_id, user_id))
        rez = self.__cursor.fetchall()
        return rez

    def get_user_privilege_in_group(self, group_id, user_id):
        sql = f"""
        SELECT
            role
        FROM
            {schema}"Participants"
        WHERE
            group_id = %s AND user_id = %s;
        """
        self.__cursor.execute(sql, (group_id, user_id))
        rez = self.__cursor.fetchone()
        return rez.get('role', None)
