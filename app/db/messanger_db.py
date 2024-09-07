from app.db.PostgresDB import PostgresDB

db = PostgresDB()


def add_message(group_id, user_id, content):
    sql = f"""
    INSERT INTO {db.schema}"Messages"
        (user_id,
        group_id,
        content)
    VALUES (%s, %s, %s)
    """
    db.execute_query(sql, (user_id, group_id, content))



def update_group(group_id, name, photo_id):
    sql = f"""
    UPDATE 
        {db.schema}"Groups"
    SET 
        name = %s, photo_id = %s
    WHERE
        id = %s  
    """
    db.execute_query(sql, (name, photo_id, group_id))



def get_user_groups(user_id):
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
    rez = db.fetch_all(sql, (user_id, user_id, user_id))
    return rez


def get_ten_last_messages(group_id):
    sql = f"""
    SELECT 
        u.username,
        m.content 
    FROM {db.schema}"Messages" m
    JOIN {db.schema}"Users" u
    ON m.user_id = u.id AND m.group_id = %s
    ORDER BY 
        created_at DESC
    LIMIT 10;
    """
    rez = db.fetch_all(sql, (group_id,))
    return rez[::-1]


def get_group_participants(group_id):
    sql = f"""
    SELECT
        user_id
    FROM {db.schema}"Participants"
    WHERE
        group_id = %s;
    """
    rez = db.fetch_all(sql, (group_id,))
    return rez


def get_user_privilege_in_group(group_id, user_id):
    sql = f"""
    SELECT
        role
    FROM
        {db.schema}"Participants"
    WHERE
        group_id = %s AND user_id = %s;
    """
    rez = db.fetch_one(sql, (group_id, user_id))
    return rez.get('role', None)


def get_group_info(group_id):
    sql = f"""
    SELECT
        pg.id as id,
        pg.name,
        pg.type,
        pg.photo_id,
        p.data as photo
    FROM
        {db.schema}"Groups" pg
    LEFT JOIN
        {db.schema}"Photos" p
    ON
        pg.photo_id = p.id
    WHERE
        pg.id = %s; 
    """
    rez = db.fetch_one(sql, (group_id,))
    return rez


def find_user_in_group(group_id, user_id):
    sql = f"""
    SELECT * FROM {db.schema}"Participants" WHERE group_id = %s AND user_id = %s;
    """
    rez = db.fetch_all(sql, (group_id, user_id))
    return rez



