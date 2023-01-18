# Модуль взаимодействия с базой данных MySql (MariaDB)
from typing import List, Dict
import pymysql
from pymysql.cursors import DictCursor


class Db:
    def __init__(self, config):

        self.conn = pymysql.connect(
            db=config['dbname'],
            user=config['user'],
            password=config['password'],
            host=config['host'],
            port=config['port'],
            charset='utf8mb4'
        )
        self.conn.autocommit = True

    # Получение одного значения
    def get_value(self, query: str, params: list = None) -> str | None:
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        if row is None:
            return None
        return row[0]

    # Получение одного кортежа
    def get_line(self, query: str, params: list = None) -> Dict:
        cursor = self.conn.cursor(cursor=DictCursor)
        cursor.execute(query, params)
        row = cursor.fetchone()
        cursor.close()
        return row

    # Получение одного столбца
    def get_row(self, query: str, params: list = None) -> List:
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        result = list()
        for row in rows:
            result.append(row[0])
        cursor.close()
        return result

    # Получение словаря (набор id->value)
    def get_dict(self, query: str, params: list = None):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        result = {}
        records = cursor.fetchall()
        for r in records:
            result[r[0]] = r[1]
        cursor.close()
        return result

    # Получение множества строк (именованные кортежи)
    def get_data(self, query: str, params: list = None):
        cursor = self.conn.cursor(cursor=DictCursor)
        cursor.execute(query, params)
        return cursor.fetchall()

    # Выполнение произвольного запроса к БД
    def execute(self, query: str, params: list = None) -> object:
        cursor = self.conn.cursor()
        result = cursor.execute(query, params)
        cursor.close()
        self.conn.commit()
        return result

    # Вставка, при использовании конструкции RETURNING - возвращает сгенерированное поле
    def insert(self, query: str, params: list = None) -> int:
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        insert_id = cursor.connection.insert_id()
        cursor.close()
        self.conn.commit()
        return insert_id
