from mysql.connector import pooling, Error
from telesql.types import *
from telesql.types.sqltypes import Column
from telesql.errors import *
from telesql.table import Table
import re



class TeleSQL:
    """
    Основной класс для подключения к MySQL и управления таблицами.

    Использование:
    ```
    from teleSQL import TeleSQL
    tele = TeleSQL(host='localhost', user='root', password='password', database='my_database')
    ```

    :param host: Адрес сервера MySQL
    :param user: Имя пользователя MySQL
    :param password: Пароль от базы
    :param database: Имя базы данных
    :param port: Порт подключения (по умолчанию 3306)
    """
    def __init__(self, host, user, password, database,port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.pool = self._create_pool()

    def _create_pool(self):
        db_config = {
            "host": self.host,
            "user": self.user,
            "password": self.password,
            "database": self.database,
            "port": self.port
        }
        return pooling.MySQLConnectionPool(
            pool_name="telesql_pool",
            pool_size=10,
            **db_config
        )
    
    def _get_conn(self):
        return self.pool.get_connection()



    def create_table(self, table_name: str, columns: dict[str, Column]):
        """
        Создает новую таблицу в базе данных.

        :param table_name: Название таблицы
        :param columns: Словарь колонок вида {'balance': sqltypes.INT(), 'refs': sqltypes.INT()}
        :return: Объект Table, привязанный к созданной таблице

        :raises TableExists: Если таблица уже существует
        :raises MySQLerr: Если произошла SQL-ошибка
        """
        conn = None
        cursor = None
        try:
            conn = self._get_conn()
            cursor = conn.cursor()

            cursor.execute("SHOW TABLES LIKE %s", (table_name,))
            if cursor.fetchone():
                raise TableExists(table_name)

            if 'id' not in columns:
                columns = {'id': sqltypes.BIGINT(primary_key=True), **columns}

            columns_sql_parts = [col._sql_string(name) for name, col in columns.items()]
            columns_sql = ",\n  ".join(columns_sql_parts)
            create_sql = f"CREATE TABLE `{table_name}` (\n  {columns_sql}\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"

            cursor.execute(create_sql)
            conn.commit()
            return Table(table_name,self,columns)
        except Error as e:
            print(f'Произошла MySQL ошибка: {e}')
            raise MySQLerr(e)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def _parse_sql_type(self,raw_type: str, *, primary_key=False, auto_increment=False,
                   nullable=False, default=None, unique=False) -> sqltypes.Column:
        raw = raw_type.lower()

        if raw.startswith("int"):
            return sqltypes.INT(primary_key=primary_key, auto_increment=auto_increment,
                            nullable=nullable, default=default, unique=unique)
        elif raw.startswith("bigint"):
            return sqltypes.BIGINT(primary_key=primary_key, auto_increment=auto_increment,
                                nullable=nullable, default=default, unique=unique)
        elif raw.startswith("smallint"):
            return sqltypes.SMALLINT(primary_key=primary_key, auto_increment=auto_increment,
                                nullable=nullable, default=default, unique=unique)
        elif raw.startswith("double"):
            return sqltypes.DOUBLE(primary_key=primary_key, auto_increment=auto_increment,
                                nullable=nullable, default=default, unique=unique)
        
        elif raw.startswith("text"):
            return sqltypes.TEXT(primary_key=primary_key,
                                nullable=nullable, default=default, unique=unique)

        elif raw.startswith("varchar") or raw.startswith("char"):
            match = re.search(r"\((\d+)\)", raw)
            length = int(match.group(1)) if match else None

            if raw.startswith("varchar"):
                return sqltypes.VARCHAR(length=length, primary_key=primary_key,
                                    nullable=nullable, default=default, unique=unique)
            else:
                return sqltypes.CHAR(length=length, primary_key=primary_key,
                                    nullable=nullable, default=default, unique=unique)
        elif raw.startswith("decimal"):
            m = re.match(r"decimal\((\d+),(\d+)\)", raw)
            if m:
                precision = int(m.group(1))
                scale = int(m.group(2))
            else:
                precision, scale = 10, 2
            return sqltypes.DECIMAL(primary_key=primary_key, auto_increment=auto_increment,
                                nullable=nullable, default=default, unique=unique,
                                precision=precision, scale=scale)
        elif raw.startswith("float"):
            return sqltypes.FLOAT(primary_key=primary_key, auto_increment=auto_increment,
                                nullable=nullable, default=default, unique=unique)
        elif raw.startswith("bool") or raw.startswith("tinyint(1)"):
            return sqltypes.BOOLEAN(primary_key=primary_key,
                                nullable=nullable, default=default, unique=unique)
        elif raw.startswith("datetime") or raw.startswith("timestamp"):
            return sqltypes.DATETIME(primary_key=primary_key,
                                    nullable=nullable, default=default, unique=unique)
        
        elif raw.startswith("date"):
            return sqltypes.DATE(primary_key=primary_key,
                                    nullable=nullable, default=default, unique=unique)
        
        else:
            return sqltypes.Column(type_=raw_type, primary_key=primary_key, auto_increment=auto_increment,
                          nullable=nullable, default=default, unique=unique)


    def get_table(self, table_name: str) -> Table:
        """
        Получает объект Table из существующей таблицы.

        :param table_name: Название таблицы
        :return: Объект Table, привязанный к найденной таблице

        :raises TableNotExists: Если таблица уже существует
        :raises MySQLerr: Если произошла SQL-ошибка
        """
        conn = None
        cursor = None
        try:
            conn = self._get_conn()
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES LIKE %s", (table_name,))
            if not cursor.fetchone():
                raise TableNotExists(table_name)
            cursor.execute(f"SHOW COLUMNS FROM `{table_name}`")
            columns_info = cursor.fetchall()
        except Error as e:
            print(f'Произошла MySQL ошибка: {e}')
            raise MySQLerr(e)

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        columns = {}
        for col in columns_info:
            name = col[0]
            raw_type = col[1]
            nullable = col[2] == 'YES'
            primary_key = col[3] == 'PRI'
            default = col[4]
            extra = col[5]
            auto_increment = 'auto_increment' in extra.lower()
            unique = False

            columns[name] = self._parse_sql_type(
                raw_type,
                primary_key=primary_key,
                auto_increment=auto_increment,
                nullable=nullable,
                default=default,
                unique=unique
            )

        return Table(name=table_name, db=self, columns=columns)

