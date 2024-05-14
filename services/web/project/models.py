from . import db


class Name(db.Model):
    """
    Абстрактная база данных для имен.

    Атрибуты:
        id (int): Первичный ключ.
        name (str): Имя, которое должно быть уникальным и не пустым.
    """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name.lower()


class Names_Man(Name):
    """Модель базы данных для мужских имен."""
    __tablename__ = 'names_man'


class Names_Woman(Name):
    """Модель базы данных для женских имен."""
    __tablename__ = 'names_woman'
