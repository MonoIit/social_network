
db = None

def init_db(database):
    global db
    db = database

def remove_participant(group_id, user_id):
    sql = f"""
    DELETE FROM 
        {db.schema}"Participants"
    WHERE 
        group_id = %s AND user_id = %s;
    """
    db.execute_query(sql, (group_id, user_id))


def lose_admin(group_id, user_id):
    sql = f"""
    UPDATE
        {db.schema}"Participants"
    SET
        role = 'participant'
    WHERE
        group_id = %s AND user_id = %s; 
    """
    db.execute_query(sql, (group_id, user_id))


def make_admin(group_id, user_id):
    sql = f"""
        UPDATE
            {db.schema}"Participants"
        SET
            role = 'admin'
        WHERE
            group_id = %s AND user_id = %s; 
        """
    db.execute_query(sql, (group_id, user_id))


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
        FROM {db.schema}"Groups" g
        JOIN {db.schema}"Participants" p ON g.id = p.group_id AND g.type = 'public'
        LEFT JOIN {db.schema}"Photos" ph ON g.photo_id = ph.id
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
        FROM {db.schema}"Participants" p1
        JOIN {db.schema}"Participants" p2 ON p1.group_id = p2.group_id AND p1.user_id = %s AND p2.user_id <> %s
        JOIN {db.schema}"Groups" g ON p1.group_id = g.id AND g.type = 'private'
        JOIN {db.schema}"Users" u ON p2.user_id = u.id
        LEFT JOIN {db.schema}"Photos" ph ON u.photo_id = ph.id
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
        p.user_id as id,
        p.role,
        u.username,
        ph.data as photo
    FROM {db.schema}"Participants" p
    JOIN {db.schema}"Users" u ON p.user_id = u.id
    LEFT JOIN {db.schema}"Photos" ph ON u.photo_id = ph.id
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


def get_friends_not_in_group(group_id, user_id):
    sql = f"""
    SELECT 
        f.friend_id AS id,
        p.role,
        u.username,
		ph.data as photo
    FROM {db.schema}"Friends" f
    LEFT JOIN {db.schema}"Participants" p ON p.user_id = f.friend_id AND p.group_id = %s
    JOIN {db.schema}"Users" u ON f.friend_id = u.id
	LEFT JOIN {db.schema}"Photos" ph ON u.photo_id = ph.id
    WHERE f.user_id = %s
        AND f.status = 'confirmed'
        AND p.role IS NULL;
    """
    rez = db.fetch_all(sql, (group_id, user_id))
    return rez


def get_first_added_user(group_id, user_id):
    sql = f"""
    SELECT
        user_id 
    FROM {db.schema}"Participants"
    WHERE group_id = %s AND user_id != %s
    ORDER BY created_at ASC
    LIMIT 1;
    """
    rez = db.fetch_one(sql, (group_id, user_id))
    return rez


def delete_group(group_id):
    sql = f"""
    DELETE FROM
        {db.schema}"Groups"
    WHERE
        id = %s;
    """
    db.execute_query(sql, (group_id,))