from app.db.PostgresDB import PostgresDB

db = PostgresDB()


def update_profile_photo(user_id, photo_id):
    sql = f"""
    UPDATE {db.schema}"Users"
    SET photo_id = %s
    WHERE id = %s
    """
    db.execute_query(sql, (photo_id, user_id))


def add_friend(from_user_id, to_user_id):
    sql = f"""
    INSERT INTO {db.schema}"Friends" VALUES (%s, %s, 'sent');
    INSERT INTO {db.schema}"Friends" VALUES (%s, %s, 'received');
    """
    db.execute_query(sql, (from_user_id, to_user_id, to_user_id, from_user_id))


def delete_friendship(user_id, friend_id):
    sql = f"""
    DELETE FROM {db.schema}"Friends"
    WHERE 
        user_id = %s AND friend_id = %s;
    """
    db.execute_query(sql, (user_id, friend_id))


def confirm_friendship(user_id, friend_id):
    sql = f"""
    UPDATE {db.schema}"Friends"
    SET status = 'confirmed'
    WHERE 
        user_id = %s AND friend_id = %s;
    """
    db.execute_query(sql, (user_id, friend_id))


def find_private_group(user1_id, user2_id):
    sql = f"""
    SELECT
        p1.group_id as id,
        g.type
    FROM {db.schema}"Participants" p1
    JOIN {db.schema}"Participants" p2
    ON
        (p1.user_id = %s AND p2.user_id = %s)
    JOIN {db.schema}"Groups" g
    ON
        p1.group_id = g.id;
    """
    rez = db.fetch_one(sql, (user1_id, user2_id))
    return rez


def get_similar_users_by_username(username):
    sql = f"""
    SELECT * FROM {db.schema}"Users" 
    WHERE username ILIKE %s;
    """
    search_username = f"%{username}%"
    rez = db.fetch_all(sql, (search_username,))
    return rez



