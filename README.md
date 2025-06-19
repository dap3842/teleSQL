# TeleSQL

TeleSQL — это Python-библиотека для управления таблицами MySQL через код. TeleSQL настроен на создание вместе с телеграмм ботами. Он позволяет создавать таблицы, а также изменять их.

## Установка

`pip install telesql`



## Примеры использования


```python
from telesql import TeleSQL
from telesql.types import sqltypes

db = TeleSQL(host='localhost',user='user',password=12345,database='database')

columns={
    'id':sqltypes.BIGINT(primary_key=True),
    'balance': sqltypes.DECIMAL(10,2),
    'refferals': sqltypes.INT(default=0)
}

table = db.create_table(table_name='Users',columns=columns)

data={
    'balance':10.42,
    'refferals': 10
}

table.add_user(id=123,data=data)

```



# Документация

## Классы

### TeleSQL

Класс для работы с базой данных Telegram.
```python
tele = TeleSQL(host='localhost', user='root', password='password', database='my_database')
```
----
Методы:

- [**TeleSQL.create_table()**](#create_tabletable_name-columns) - создает таблицу в базе данных.
- [**TeleSQL.get_table()**](#get_tabletable_namr) - получает [`Table`](#table) по имени таблицы.
-----
### Table


Класс для работы с таблицей

```python
table = TeleSQL.create_table('table',columns) # type: Table
```
----
Методы:
- [**Table.add_user()**](#add_useriddata)  - добавляет пользователя в таблицу

- [**Table.user_exists()**](#user_existsid) - проверяет существует ли пользователь в таблице

- [**Table.update_user_set()**](#update_user_setidcolumnvalue) - обновляет значения в таблице

- [**Table.update_user_add()**](#update_user_addidcolumnadd_value) - увеличивает значение в таблице

- [**Table.update_user_sub()**](#update_user_subidcolumnsub_value) - уменьшает значение в таблице

- [**Table.get_column_user()**](#get_column_useridcolumn) - получает значение пользователя по столбцу

- [**Table.delete_user()**](#delete_userid) - удаляет пользователя из таблицы

- [**Table.get_user()**](#get_userid) - получает пользователя по id

- [**Table.get_all_users()**](#get_all_users) - получает всех пользователей

- [**Table.filter_users_less()**](#filter_users_lesscolumnvalue) - получает пользователей по условию (меньше заданного значения)

- [**Table.filter_users_more()**](#filter_users_lesscolumnvalue) - получает пользователей по условию (больше заданного значения)

- [**Table.filter_users_equal()**](#filter_users_lesscolumnvalue) - получает пользователей по условию (равно заданному значению)

------

## Методы

### `create_table(table_name, columns)`

Создает новую таблицу в базе данных.

- **table_name** - `str` имя таблицы

- **columns** -   `dict` словарь объектов `sqltypes` с именами столбцов и их типами.



Возвращает объект [`Table`](#table)

----
### `get_table(table_namr)`

Получает объект [`Table`](#table) из существующей таблицы.

- **table_name** - `str` имя таблицы.



Возвращает объект [`Table`](#table)

-----

### `add_user(id,data)`

Добавляет нового пользователя в таблицу.

- **id** - `int` Telegram ID пользователя

- **data** - `dict` словарь с данными пользователя.


### `user_exists(id)`

Проверяет на наличие пользователя в таблице.

- **id** - `int` Telegram ID пользователя.

Возвращает `True` если пользователь есть в таблица, `False` в противном случае.

-----

### `update_user_set(id,column,value)`

Устанавливает значение в ячейке таблицы.

- **id** - `int` Telegram ID пользователя.
- **column** - `str` имя столбца.
- **value** - {в зависимости от типа столбца} значение ячейки.

-----

### `update_user_add(id,column,add_value)`

Увеличивает значение в ячейке таблицы.

- **id** - `int` Telegram ID пользователя.
- **column** - `str` имя столбца.
- **add_value** - `int | float` Значение для увеличения
-----

### `update_user_sub(id,column,sub_value)`

Уменьшает значение в ячейке таблицы.
Обертка для update_user_add

- **id** - `int` Telegram ID пользователя.
- **column** - `str` имя столбца.
- **sub_value** - `int | float` Значение для уменьшения
-----


### `get_column_user(id,column)`

Получает значение из ячейки таблицы.

- **id** - `int` Telegram ID пользователя.
- **column** - `str` имя столбца.

Возвращает значение ячейки.

-----
### `delete_user(id)`

Удаление пользователя по id

- **id** - `int` Telegram ID пользователя.
-----
### `get_user(id)`

Получает данные пользователя по ID.

- **id** - `int` Telegram ID пользователя.

Возвращает словарь значений всех колонок для этого пользователя

-----
### `get_all_users()`

Получает данные всех пользователей.

Возвращает список словарей значений всех колонок для каждого пользователя

----

### `filter_users_less(column,value)`

Получает данные отфилированных пользователей по заданному условию.(меньше заданного значения)

Аналоги

- filter_users_more(column,value) - больше заданного значения
- filter_users_equal(column,value) - равно заданному значению

---


- **column** - `str` имя столбца.
- **value** - `int | float` значение.



-----





## Типы данных

Поддерживаемые типы данных:
- **INT**
- **BIGINT**
- **SMALLINT**
- **FLOAT**
- **DECIMAL**
- **DOUBLE**
- **TEXT**
- **VARCHAR**
- **CHAR**
- **DATE**
- **DATETIME**
- **BOOLEAN**
----
Пример указания типа при создании таблицы:
```python
columns={
    'id': sqltypes.INT(primary_key=True)
    'balance': sqltypes.DECIMAL(10,2,nullable=False,default=0)
}
```

Возможные аргументы для всех типов:

- **primary_key=True** - указывает, что столбец является первичным ключом таблиц
- **nullable=False** - указывает, что столбец не может быть null
- **default=0** - указывает значение по умолчанию для столбца
- **unique=True** - указывает, что значение уникально для каждого пользователя

----

#### Для типов `INT`, `BIGINT`, `SMALLINT` доступны следующие аргументы:

- **auto_increment=True** - указывает, что столбец будет автоматически увеличиваться

#### Для типов `FLOAT`, `DECIMAL`, `DOUBLE` доступны следующие аргументы:
- **scale=2** - указывает количество знаков после запятой
- **precision=10** - указывает общее количество знаков(для `DECIMAL`)

#### Для типов `TEXT`, `VARCHAR`, `CHAR` доступны следующие аргументы:

- **length=255** - указывает длину строки










