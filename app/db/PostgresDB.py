import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config

schema = 'sn.'


class PostgresDB:

    def __init__(self):
        self.__db = psycopg2.connect(
            host=Config.DB_HOST,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        self.__cursor = self.__db.cursor(cursor_factory=RealDictCursor)
        self.schema = "sn."

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
        return self.__cursor.fetchone()

    def fetch_all(self, query, params=None):
        """
        Выполняет SQL-запрос и возвращает все строки.
        :param query: SQL-запрос.
        :param params: Параметры для SQL-запроса.
        :return: Список словарей с данными строк.
        """
        self.execute_query(query, params)
        return self.__cursor.fetchall()

    def close(self):
        """
        Закрывает курсор и соединение с базой данных.
        """
        self.__cursor.close()
        self.__db.close()







