from app.methods import PostgresDB, shared_db, feed_db, friends_db, messanger_db, users_db

db = PostgresDB.PostgresDB()
shared_db.init_db(db)
feed_db.init_db(db)
friends_db.init_db(db)
messanger_db.init_db(db)
users_db.init_db(db)