from datetime import datetime,date
class Column():
    """
    Класс для описания столбца таблицы.

    .. warning::
        Данный класс не предназначен для прямого использования.
        Рекомендуется создавать столбцы с помощью готовых типов из модуля `sqltypes`, например `sqltypes.INT()`.

    Пример:
        ```
        from telesql.types import sqltypes
        balance = sqltypes.INT(primary_key=True)
        ```
    """

    def __init__(self,type_, *,primary_key=False,auto_increment=False,
                 nullable=False, default=None, unique=False):
        self.type = type_
        self.primary_key = primary_key
        self.auto_increment = auto_increment
        self.nullable = nullable
        self.default = default
        self.unique = unique

    def __repr__(self):
        return f"<{self.__class__.__name__} pk={self.primary_key}>"

    def _sql_string(self, name):
        parts = [f"{name} {self.type}"]
        if self.primary_key:
            parts.append("PRIMARY KEY")
        if self.auto_increment:
            parts.append("AUTO_INCREMENT")
        if not self.nullable:
            parts.append("NOT NULL")
        if self.default is not None:
            if isinstance(self.default, str):
                parts.append(f"DEFAULT '{self.default}'")
            else:
                parts.append(f"DEFAULT {self.default}")
        if self.unique:
            parts.append("UNIQUE")
        return " ".join(parts)
    
class DECIMAL(Column):
    """
    Класс для описания столбца типа DECIMAL.

    Пример:
        ```
        from telesql.types import sqltypes
        price = sqltypes.DECIMAL(primary_key=False, nullable=True, default=0.0)
        ```

    :param primary_key: Если True, то столбец является первичным ключом.
    :type primary_key: bool
    :param auto_increment: Если True, то столбец будет автоматически увеличиваться (для DECIMAL обычно False).
    :type auto_increment: bool
    :param nullable: Если True, то столбец может быть null.
    :type nullable: bool
    :param default: Значение по умолчанию для столбца.
    :type default: float | None
    :param unique: Если True, то столбец будет уникальным.
    :type unique: bool
    :param precision: Общая точность числа (всего цифр).
    :type precision: int
    :param scale: Количество цифр после запятой.
    :type scale: int
    """
    def __init__(
        self,
        precision: int = 10,
        scale: int = 2,
        *,
        primary_key: bool = False,
        auto_increment: bool = False,
        nullable: bool = False,
        default: float | None = None,
        unique: bool = False
        
    ):
        self.precision = precision
        self.scale = scale
        super().__init__(
            f"DECIMAL({self.precision},{self.scale})",
            primary_key=primary_key,
            auto_increment=auto_increment,
            nullable=nullable,
            default=default,
            unique=unique
        )

class INT(Column):
    """
    Класс для описания столбца типа INT.

    Пример:
        ```
        from telesql.types import sqltypes
        balance = sqltypes.INT(primary_key=True)
        ```

    :param primary_key: Если True, то столбец является первичным ключом.
    :type primary_key: bool
    :param auto_increment: Если True, то столбец будет автоматически увеличиваться
    :type auto_increment: bool
    :param nullable: Если True, то столбец может быть null.
    :type nullable: bool
    :param default: Значение по умолчанию для столбца.
    :type default: int
    :param unique: Если True, то столбец будет уникальным.
    :type unique: bool
    """
    def __init__(
        self,
        primary_key: bool = False,
        auto_increment: bool = False,
        nullable: bool = False,
        default: int | None =None,
        unique: bool = False
    ):
        super().__init__(
            "INT",
            primary_key=primary_key,
            auto_increment=auto_increment,
            nullable=nullable,
            default=default,
            unique=unique
        )
    

class BIGINT(Column):
    """
    Класс для описания столбца типа BIGINT.

    Пример:
        ```
        from telesql.types import sqltypes
        balance = sqltypes.BIGINT(primary_key=True)
        ```

    :param primary_key: Если True, то столбец является первичным ключом.
    :type primary_key: bool
    :param auto_increment: Если True, то столбец будет автоматически увеличиваться
    :type auto_increment: bool
    :param nullable: Если True, то столбец может быть null.
    :type nullable: bool
    :param default: Значение по умолчанию для столбца.
    :type default: int
    :param unique: Если True, то столбец будет уникальным.
    :type unique: bool
    """
    def __init__(
        self,
        primary_key: bool = False,
        auto_increment: bool = False,
        nullable: bool = False,
        default: int | None = None,
        unique: bool = False
    ):
        super().__init__(
            "BIGINT",
            primary_key=primary_key,
            auto_increment=auto_increment,
            nullable=nullable,
            default=default,
            unique=unique
        )

class SMALLINT(Column):
    """
    Класс для описания столбца типа SMALLINT.

    Пример:
        ```
        from telesql.types import sqltypes
        balance = sqltypes.SMALLINT(primary_key=True)
        ```

    :param primary_key: Если True, то столбец является первичным ключом.
    :type primary_key: bool
    :param auto_increment: Если True, то столбец будет автоматически увеличиваться
    :type auto_increment: bool
    :param nullable: Если True, то столбец может быть null.
    :type nullable: bool
    :param default: Значение по умолчанию для столбца.
    :type default: int
    :param unique: Если True, то столбец будет уникальным.
    :type unique: bool
    """
    def __init__(
        self,
        primary_key: bool = False,
        auto_increment: bool = False,
        nullable: bool = False,
        default: int | None = None,
        unique: bool = False
    ):
        super().__init__(
            "SMALLINT",
            primary_key=primary_key,
            auto_increment=auto_increment,
            nullable=nullable,
            default=default,
            unique=unique
        )

class FLOAT(Column):
    """
    Класс для описания столбца типа FLOAT.

    Пример:
        ```
        from telesql.types import sqltypes
        balance = sqltypes.FLOAT(nullable=True)
        ```

    :param primary_key: Если True, то столбец является первичным ключом.
    :type primary_key: bool
    :param auto_increment: Если True, то столбец будет автоматически увеличиваться
    :type auto_increment: bool
    :param nullable: Если True, то столбец может быть null.
    :type nullable: bool
    :param default: Значение по умолчанию для столбца.
    :type default: int или float
    :param unique: Если True, то столбец будет уникальным.
    :type unique: bool
    """
    def __init__(
        self,
        primary_key: bool = False,
        auto_increment: bool = False,
        nullable: bool = False,
        default: int | float | None = None,
        unique: bool = False
    ):
        super().__init__(
            "FLOAT",
            primary_key=primary_key,
            auto_increment=auto_increment,
            nullable=nullable,
            default=default,
            unique=unique
        )

class DOUBLE(Column):
    """
    Класс для описания столбца типа DOUBLE.

    Пример:
        ```
        from telesql.types import sqltypes
        balance = sqltypes.DOUBLE(nullable=True)
        ```

    :param primary_key: Если True, то столбец является первичным ключом.
    :type primary_key: bool
    :param auto_increment: Если True, то столбец будет автоматически увеличиваться
    :type auto_increment: bool
    :param nullable: Если True, то столбец может быть null.
    :type nullable: bool
    :param default: Значение по умолчанию для столбца.
    :type default: int или float
    :param unique: Если True, то столбец будет уникальным.
    :type unique: bool
    """
    def __init__(
        self,
        primary_key: bool = False,
        auto_increment: bool = False,
        nullable: bool = False,
        default: int | float | None = None,
        unique: bool = False
    ):
        super().__init__(
            "DOUBLE",
            primary_key=primary_key,
            auto_increment=auto_increment,
            nullable=nullable,
            default=default,
            unique=unique
        )


class TEXT(Column):
    """
    Класс для описания столбца типа TEXT.

    Пример:
        ```
        from telesql.types import sqltypes
        balance = sqltypes.TEXT(nullable=True)
        ```

    :param primary_key: Если True, то столбец является первичным ключом.
    :type primary_key: bool
    :param nullable: Если True, то столбец может быть null.
    :type nullable: bool
    :param default: Значение по умолчанию для столбца.
    :type default: str
    :param unique: Если True, то столбец будет уникальным.
    :type unique: bool
    """
    def __init__(
        self,
        *,
        primary_key: bool = False,
        nullable: bool = False,
        default: str | None = None,
        unique: bool = False
    ):
        super().__init__(
            "TEXT",
            primary_key=primary_key,
            auto_increment=False,
            nullable=nullable,
            default=default,
            unique=unique
        )

class VARCHAR(Column):
    """
    Класс для описания столбца типа VARCHAR.

    Пример:
        ```
        from telesql.types import sqltypes
        balance = sqltypes.VARCHAR(30,nullable=True)
        ```
    :param lenght: Длина столбца.
    :type lenght: int
    :param primary_key: Если True, то столбец является первичным ключом.
    :type primary_key: bool
    :param nullable: Если True, то столбец может быть null.
    :type nullable: bool
    :param default: Значение по умолчанию для столбца.
    :type default: str
    :param unique: Если True, то столбец будет уникальным.
    :type unique: bool
    """
    def __init__(
        self,
        length: int,
        *,
        primary_key: bool = False,
        nullable: bool = False,
        default: str | None = None,
        unique: bool = False
    ):
        super().__init__(
            f"VARCHAR({length})",
            primary_key=primary_key,
            auto_increment=False,
            nullable=nullable,
            default=default,
            unique=unique
        )

class CHAR(Column):
    """
    Класс для описания столбца типа CHAR.

    Пример:
        ```
        from telesql.types import sqltypes
        balance = sqltypes.CHAR(30,nullable=True)
        ```
    :param lenght: Длина столбца.
    :type lenght: int
    :param primary_key: Если True, то столбец является первичным ключом.
    :type primary_key: bool
    :param nullable: Если True, то столбец может быть null.
    :type nullable: bool
    :param default: Значение по умолчанию для столбца.
    :type default: str
    :param unique: Если True, то столбец будет уникальным.
    :type unique: bool
    """
    def __init__(
        self,
        length: int,
        *,
        primary_key: bool = False,
        nullable: bool = False,
        default: str | None = None,
        unique: bool = False
    ):
        super().__init__(
            f"CHAR({length})",
            primary_key=primary_key,
            auto_increment=False,
            nullable=nullable,
            default=default,
            unique=unique
        )


class DATE(Column):
    """
    Класс для описания столбца типа DATE.

    Пример:
        ```
        from telesql.types import sqltypes
        balance = sqltypes.DATE(nullable=True)
        ```
    :param lenght: Длина столбца.
    :type lenght: int
    :param primary_key: Если True, то столбец является первичным ключом.
    :type primary_key: bool
    :param nullable: Если True, то столбец может быть null.
    :type nullable: bool
    :param default: Значение по умолчанию для столбца.
    :type default: date
    :param unique: Если True, то столбец будет уникальным.
    :type unique: bool
    """
    def __init__(
        self,
        primary_key: bool = False,
        nullable: bool = False,
        default: date | None = None,
        unique: bool = False
    ):
        super().__init__(
            "DATE",
            primary_key=primary_key,
            auto_increment=False,
            nullable=nullable,
            default=default,
            unique=unique
        )

class DATETIME(Column):
    """
    Класс для описания столбца типа DATETIME.

    Пример:
        ```
        from telesql.types import sqltypes
        balance = sqltypes.DATETIME(nullable=True)
        ```
    :param lenght: Длина столбца.
    :type lenght: int
    :param primary_key: Если True, то столбец является первичным ключом.
    :type primary_key: bool
    :param nullable: Если True, то столбец может быть null.
    :type nullable: bool
    :param default: Значение по умолчанию для столбца.
    :type default: datetime
    :param unique: Если True, то столбец будет уникальным.
    :type unique: bool
    """
    def __init__(
        self,
        primary_key: bool = False,
        nullable: bool = False,
        default: datetime | None = None,
        unique: bool = False
    ):
        super().__init__(
            "DATETIME",
            primary_key=primary_key,
            auto_increment=False,
            nullable=nullable,
            default=default,
            unique=unique
        )

class BOOLEAN(Column):
    """
    Класс для описания столбца типа BOOLEAN.

    Пример:
        ```
        from telesql.types import sqltypes
        balance = sqltypes.BOOLEAN(nullable=True)
        ```
    :param lenght: Длина столбца.
    :type lenght: int
    :param primary_key: Если True, то столбец является первичным ключом.
    :type primary_key: bool
    :param nullable: Если True, то столбец может быть null.
    :type nullable: bool
    :param default: Значение по умолчанию для столбца.
    :type default: bool
    :param unique: Если True, то столбец будет уникальным.
    :type unique: bool
    """
    def __init__(
        self,
        primary_key: bool = False,
        nullable: bool = False,
        default: bool | None = None,
        unique: bool = False
    ):
        super().__init__(
            "TINYINT(1)",
            primary_key=primary_key,
            auto_increment=False,
            nullable=nullable,
            default=default,
            unique=unique
        )