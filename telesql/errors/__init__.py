

class TableExists(Exception):
    def __init__(self, name):
        super().__init__(f"Таблица с именем {name} уже существует")

class TableNotExists(Exception):
    def __init__(self, name):
        super().__init__(f"Таблица с именем {name} не существует")


class MySQLerr(Exception):
    def __init__(self, error):
        super().__init__(f"Ошибка в создании таблицы: {error}")


class UserNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)