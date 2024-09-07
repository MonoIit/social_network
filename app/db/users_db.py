from app.db.PostgresDB import PostgresDB
from app.db.PostgresDB import schema

db = PostgresDB()


def get_user_by_username(username):
    sql = f"""
    SELECT 
        id,
        username,
        email,
        password,
        photo_id
    FROM {db.schema}"Users"
    WHERE username = %s
    LIMIT 1;
    """
    rez = db.fetch_one(sql, (username,))
    return rez


def create_user(username, email, password, photo_id):
    sql = f"""
    INSERT INTO {schema}"Users" 
        (username,
        email,
        password,
        photo_id)
    VALUES 
        (%s, %s, %s, %s);
    """
    db.execute_query(sql, (username, email, password, photo_id))
