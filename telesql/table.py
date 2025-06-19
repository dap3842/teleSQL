from telesql.types import sqltypes
from telesql.errors import *
from mysql.connector import Error
import datetime

class Table():
    '''
    Класс для работы с таблицей
    '''
    def __init__(self, name,db,columns: dict[str,sqltypes.Column]):
        self.name=name
        self.db = db
        self.columns = columns

    
    def add_user(self,id,data: dict):
        """
        Добавляет нового пользователя в таблицу.

        :param id: Telegram ID пользователя
        :param data: Словарь значений колонок
        :raises ValueError: Если не переданы обязательные поля
        """
        columns = self.columns #dict[str,Column]
        insert_data={}
        for col_name, col_obj in columns.items():
            if col_obj.auto_increment:
                continue
            if col_name == 'id':
                insert_data['id'] = id
            if col_name in data:
                insert_data[col_name] = data[col_name]
            elif col_obj.default is not None:
                insert_data[col_name] = col_obj.default
            elif col_obj.nullable:
                insert_data[col_name] = None
            else:
                if col_name == 'id':
                    continue
                else:
                    raise ValueError(f"Missing required field: {col_name}")
        
        conn = None
        cursor = None

        try:
            conn = self.db._get_conn()
            cursor = conn.cursor()
            colnames = ', '.join(i for i in insert_data)
            procenti = ', '.join(['%s']*len(insert_data))
            query = f"""INSERT INTO {self.name} ({colnames}) VALUES ({procenti})"""
            val = tuple(insert_data.values())
            cursor.execute(query,val)
            conn.commit()
        except Error as e:
            print(f'Произошла MySQL ошибка: {e}')
            raise MySQLerr(e)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def user_exists(self,id) -> bool:
        """
        Проверяет на наличие пользователя в таблице.

        :param id: Telegram ID пользователя
        :return: True если пользователь существует, False в противном случае
        """
        conn = None
        cursor = None
        try:
            conn = self.db._get_conn()
            cursor = conn.cursor()
            query = f"SELECT * FROM {self.name} WHERE id = %s"
            cursor.execute(query, (id,))
            if cursor.fetchone():
                return True
            else:
                return False
        except Error as e:
            print(f'Произошла MySQL ошибка: {e}')
            raise MySQLerr(e)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_user_set(self, id, column,value):
        """
        Устанавливает значение в ячейке таблицы.

        :param: id: Айди пользователя
        :param column: Название колонки
        :param value: Значение для установки
        :raises TypeError: При неправильном типе данных
        """
        if column not in self.columns:
            raise ValueError(f"Нет столбца {column}")
        elif not self._can_update_column(value,column):
            raise TypeError(f"Нельзя обновить колонку {column} значением {value}")
        conn = None
        cursor = None
        try:
            conn = self.db._get_conn()
            cursor = conn.cursor()
            query = f"UPDATE {self.name} SET {column} = %s WHERE id = %s"
            cursor.execute(query, (value,id))
            conn.commit()
        except Error as e:
            print(f'Произошла MySQL ошибка: {e}')
            raise MySQLerr(e)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    




    def update_user_add(self,id,column,add_value):
        """
        Увеличивает значение в ячейке таблицы.

        :param: id: Айди пользователя
        :param column: Название колонки
        :param value: Значение для увеличения
        :raises TypeError: При неправильном типе данных
        """
        if column not in self.columns:
            raise ValueError(f"Нет столбца {column}")
        elif not self._can_update_column(add_value,column):
            raise TypeError(f"Нельзя обновить колонку {column} значением {add_value}")
        elif not isinstance(add_value, (int, float)):
            raise TypeError(f"Нельзя обновить колонку {column} значением {add_value}")
        conn = None
        cursor = None
        try:
            conn = self.db._get_conn()
            cursor = conn.cursor()
            
            query = f"UPDATE {self.name} SET {column} = {column} + %s WHERE id = %s"
            cursor.execute(query, (add_value,id))
            conn.commit()
        except Error as e:
            print(f'Произошла MySQL ошибка: {e}')
            raise MySQLerr(e)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            
    def update_user_sub(self,id,column,sub_value):
        """
        Уменьшает значение в ячейке таблицы.

        Обертка для update_user_add

        :param: id: Айди пользователя
        :param column: Название колонки
        :param value: Значение для уменьшения
        :raises TypeError: При неправильном типе данных
        """
        self.update_user_add(id,column,-sub_value)


    def get_column_user(self,id,column):
        """
        Получает значение из ячейки таблицы.

        :param id: Айди пользователя
        :param column: Название колонки
        :return: Значение из ячейки
        :raises UserNotFound: Если пользователь не найден
        """
        conn = None
        cursor = None
        try:
            conn = self.db._get_conn()
            cursor = conn.cursor()
            query = f"SELECT {column} FROM {self.name} WHERE id = %s"
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                raise UserNotFound(f"Пользователь с id {id} не найден")
        except Error as e:
            print(f'Произошла MySQL ошибка: {e}')
            raise MySQLerr(e)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()



    def _can_update_column(self, val, column: str) -> bool:
        col_type = self.columns[column].type.upper()

        try:
            if col_type in ["INT", "BIGINT", "SMALLINT"]:
                int(val)
            elif col_type in ["FLOAT", "DOUBLE", "DECIMAL"]:
                float(val)
            elif col_type in ["TEXT", "VARCHAR", "CHAR"]:
                str(val)
            elif col_type in ["BOOLEAN", "BOOL", "TINYINT(1)"]:
                if isinstance(val, bool) or val in [0, 1, '0', '1', 'true', 'false', 'True', 'False']:
                    return True
                return False
            elif col_type in ["DATE", "DATETIME", "TIMESTAMP"]:
                
                if isinstance(val, datetime.date) or isinstance(val, str):
                    return True
                return False
            else:
                return False
            return True
        except (ValueError, TypeError):
            return False

    def delete_user(self,id):
        """
        Удаление пользователя по id

        :param id: Айди пользователя для удаления
        """
        conn = None
        cursor = None
        try:
            conn = self.db._get_conn()
            cursor = conn.cursor()
            query = f"DELETE FROM {self.name} WHERE id = %s"
            cursor.execute(query, (id,))
            conn.commit()
        except Error as e:
            print(f'Произошла MySQL ошибка: {e}')
            raise MySQLerr(e)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_user(self,id):
        """
        Получает данные пользователя по ID.

        :param id: Telegram ID
        :return: Словарь значений всех колонок для этого пользователя
        :raises UserNotFound: Если пользователь не найден
        """
        conn = None
        cursor = None
        try:
            conn = self.db._get_conn()
            cursor = conn.cursor(dictionary=True)
            query = f"SELECT * FROM {self.name} WHERE id = %s"
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            if row:
                return row
            else:
                raise UserNotFound(f"Пользователь с id {id} не найден")
        except Error as e:
            print(f'Произошла MySQL ошибка: {e}')
            raise MySQLerr(e)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    
    def get_all_users(self):
        """
        Получает данные всех пользователей.
        """
        conn = None
        cursor = None
        try:
            conn = self.db._get_conn()
            cursor = conn.cursor(dictionary=True)
            query = f"SELECT * FROM {self.name}"
            cursor.execute(query)
            rows = cursor.fetchall()
            users = []
            for row in rows:
                users.append(row)
            return users
        except Error as e:
            print(f'Произошла MySQL ошибка: {e}')
            raise MySQLerr(e)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    

    def filter_users_less(self,column,value):
        """
        Получает данные отфилированных пользователей по заданному условию.

        Возвращает список словарей с данными пользователей, где значение в заданном столбце меньше заданного значения.

        :param column: Название столбца.
        :param value: Значение, которое должно быть меньше.
        """
        conn = None
        cursor = None
        try:
            conn = self.db._get_conn()
            cursor = conn.cursor(dictionary=True)
            query = f"SELECT * FROM {self.name} WHERE {column} < {value}"
            cursor.execute(query)
            rows = cursor.fetchall()
            users = []
            for row in rows:
                users.append(row)
            return users
        except Error as e:
            print(f'Произошла MySQL ошибка: {e}')
            raise MySQLerr(e)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def filter_users_more(self,column,value):
        """
        Получает данные отфилированных пользователей по заданному условию.

        Возвращает список словарей с данными пользователей, где значение в заданном столбце больше заданного значения.

        :param column: Название столбца.
        :param value: Значение, которое должно быть больше.
        """
        conn = None
        cursor = None
        try:
            conn = self.db._get_conn()
            cursor = conn.cursor(dictionary=True)
            query = f"SELECT * FROM {self.name} WHERE {column} > {value}"
            cursor.execute(query)
            rows = cursor.fetchall()
            users = []
            for row in rows:
                users.append(row)
            return users
        except Error as e:
            print(f'Произошла MySQL ошибка: {e}')
            raise MySQLerr(e)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def filter_users_equal(self,column,value):
        """
        Получает данные отфилированных пользователей по заданному условию.

        Возвращает список словарей с данными пользователей, где значение в заданном столбце равно заданному значению.

        :param column: Название столбца.
        :param value: Значение, которое должно быть равно.
        """
        conn = None
        cursor = None
        try:
            conn = self.db._get_conn()
            cursor = conn.cursor(dictionary=True)
            query = f"SELECT * FROM {self.name} WHERE {column} = {value}"
            cursor.execute(query)
            rows = cursor.fetchall()
            users = []
            for row in rows:
                users.append(row)
            return users
        except Error as e:
            print(f'Произошла MySQL ошибка: {e}')
            raise MySQLerr(e)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    