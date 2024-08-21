import os

class Config:
    SECRET_KEY = '1234'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:1337@localhost/sn')
    SQLALCHEMY_TRACK_MODIFICATIONS = False