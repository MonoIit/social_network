from app.db.PostgresDB import PostgresDB

db = PostgresDB()


def get_posts():
    sql = f"""
    SELECT 
        p.id AS post_id,
        u.id AS author_id,
        u.username AS author_username,
        p.message AS message,
        p1.data AS post_photo,
        p2.data AS user_photo
    FROM 
        {db.schema}"Posts" p 
    LEFT JOIN 
        {db.schema}"Photos_Posts" pp ON pp."Posts_id"= p.id
    JOIN 
        {db.schema}"Users" u ON p.author_id = u.id
    LEFT JOIN
        {db.schema}"Photos" p1 ON pp."Photos_id" = p1.id
    LEFT JOIN
        {db.schema}"Photos" p2 ON u.photo_id = p2.id
    ORDER BY 
        p.id
    LIMIT 10;
    """
    rez = db.fetch_all(sql)
    return rez


def __connect_image_to_post(post_id, image_id):
    sql = f"""
    INSERT INTO {db.schema}"Photos_Posts"
        ("Photos_id",
        "Posts_id")
    VALUES
        (%s, %s);
    """
    db.execute_query(sql, (image_id, post_id))


def create_post(author_id, message, image_id):
    sql = f"""
    INSERT INTO {db.schema}"Posts"
        (author_id,
        message)
    VALUES
        (%s, %s)
    RETURNING id;
    """
    post = db.fetch_one(sql, (author_id, message))
    if post:
        post_id = post['id']
        if image_id:
            __connect_image_to_post(post_id=post_id, image_id=image_id)



