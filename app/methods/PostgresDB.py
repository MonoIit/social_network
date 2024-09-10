import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
load_dotenv()

schema = 'sn.'


class PostgresDB:

    def __init__(self):
        self.__db = psycopg2.connect(
            host=os.getenv('POSTGRESS_DB_HOST', 'db'),
            port=os.getenv('POSTGRESS_DB_PORT', 5432),
            database=os.getenv('POSTGRESS_DB_NAME'),
            user=os.getenv('POSTGRESS_DB_USER'),
            password=os.getenv('POSTGRESS_DB_PASSWORD')
        )
        self.__cursor = self.__db.cursor(cursor_factory=RealDictCursor)
        self.schema = "public."

    def execute_query(self, query, params=None):
        """
        Выполняет SQL-запрос с необязательными параметрами.
        :param query: SQL-запрос.
        :param params: Параметры для SQL-запроса.
        """
        try:
            self.__cursor.execute(query, params)
            self.__db.commit()
        except Exception as e:
            self.__db.rollback()
            print(f"[!] Error executing query: {e}")

    def fetch_one(self, query, params=None):
        """
        Выполняет SQL-запрос и возвращает одну строку.
        :param query: SQL-запрос.
        :param params: Параметры для SQL-запроса.
        :return: Словарь с данными строки.
        """
        self.execute_query(query, params)
        try:
            rez = self.__cursor.fetchone()
        except Exception as e:
            rez = None
        return rez

    def fetch_all(self, query, params=None):
        """
        Выполняет SQL-запрос и возвращает все строки.
        :param query: SQL-запрос.
        :param params: Параметры для SQL-запроса.
        :return: Список словарей с данными строк.
        """
        self.execute_query(query, params)
        try:
            rez = self.__cursor.fetchall()
        except Exception as e:
            rez = []
        return rez

    def close(self):
        """
        Закрывает курсор и соединение с базой данных.
        """
        self.__cursor.close()
        self.__db.close()







