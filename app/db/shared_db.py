from app.db.PostgresDB import PostgresDB


db = PostgresDB()


def add_user_to_group(user_id, group_id, role):
    sql = f"""
    INSERT INTO {db.schema}"Participants"
        (user_id,
        group_id,
        role)
    VALUES (%s, %s, %s);
    """
    db.execute_query(sql, (user_id, group_id, role))


def create_group(name, photo_id, type):
    sql = f"""
    INSERT INTO {db.schema}"Groups"
        (name,
        photo_id,
        type)
    VALUES (%s, %s, %s)
    RETURNING id;
    """
    rez = db.fetch_one(sql, (name, photo_id, type))
    return rez


def get_user_by_id(user_id):
    sql = f"""
    SELECT 
        u.id as id,
        username,
        email,
        photo_id,
        data as photo
    FROM {db.schema}"Users" u
    LEFT JOIN {db.schema}"Photos" p 
        ON photo_id = p.id
    WHERE u.id = %s;
    """
    rez = db.fetch_one(sql, (user_id,))
    return rez


def add_image_and_get_id(name, data):
    sql = f"""
    INSERT INTO {db.schema}"Photos" 
        (filename, 
        data) 
    VALUES 
        (%s, %s) 
    RETURNING id;
    """
    rez = db.fetch_all(sql, (name, data))
    return rez


def find_friendship(from_user_id, to_user_id):
    sql = f"""
    SELECT status FROM {db.schema}"Friends" 
    WHERE 
        user_id = %s AND friend_id = %s;
    """
    rez = db.fetch_one(sql, (from_user_id, to_user_id))
    return rez


def get_friends_by_id(from_user_id):
    sql = f"""
    WITH UserFriends AS (
        -- Находим всех друзей пользователя
        SELECT 
            f.friend_id,
            f.status,
            u.username,
            p.data as photo
        FROM {db.schema}"Friends" f
        JOIN {db.schema}"Users" u ON f.friend_id = u.id
        LEFT JOIN sn."Photos" p ON u.photo_id = p.id
        WHERE (f.user_id = %s)
    ),
    PrivateGroups AS (
        -- Находим группы типа 'private', в которых участвуют друзья пользователя
        SELECT 
            p1.user_id,
            g.id AS group_id
        FROM {db.schema}"Groups" g
        JOIN {db.schema}"Participants" p1 ON g.id = p1.group_id  -- Проверяем участие друга
        JOIN {db.schema}"Participants" p2 ON g.id = p2.group_id  -- Проверяем участие пользователя
        WHERE g.type = 'private' 
          AND p1.user_id IN (SELECT friend_id FROM UserFriends)  -- Друг в группе
          AND p2.user_id = %s  -- Пользователь в группе
    )
    SELECT 
        uf.friend_id as id,
        uf.username,
        uf.status,
        uf.photo,
        pg.group_id
    FROM UserFriends uf
    LEFT JOIN PrivateGroups pg ON pg.user_id = uf.friend_id;
    """
    rez = db.fetch_all(sql, (from_user_id, from_user_id))
    return rez
