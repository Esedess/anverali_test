import click
from flask import json

from . import app, db
from .models import Names_Man, Names_Woman


@app.cli.command('create_db')
def create_db():
    """Функция создания базы данных."""
    try:
        db.create_all()
        msg = 'База данных успешно создана'
        app.logger.info(msg)
        click.echo(msg)
    except Exception as e:
        click.echo(f'Ошибка при создании базы данных: {e}')


@app.cli.command('drop_db')
def drop_db():
    """Функция удаления таблиц базы данных."""
    if click.confirm(
            'Вы уверены, что хотите удалить все таблицы базы данных?'):
        db.drop_all()
        msg = 'Таблицы базы данных успешно удалены'
        app.logger.warning(msg)
        click.echo(msg)
    else:
        click.echo('Отменено.')


def load_names_from_json(filename):
    """
    Загружает имена из JSON файла.

    Args:
        filename (str): Путь к JSON файлу.

    Returns:
        dict: Данные, загруженные из JSON файла.
    """
    with open(filename) as json_file:
        return json.load(json_file)


def add_names_to_database(names, model):
    """
    Добавляет список имен в базу данных, используя указанную модель.

    Args:
        names (list): Список имен для добавления в базу данных.
        model (db.Model): Модель базы данных для добавления имен.
    """
    for name in names:
        db.session.add(model(name=name))


@app.cli.command('seed_db')
def seed_db():
    """Функция наполнения таблиц базы данных."""
    try:
        female_names = load_names_from_json('data/female_names.json')
        male_names = load_names_from_json('data/male_names.json')

        add_names_to_database(female_names, Names_Woman)
        add_names_to_database(male_names, Names_Man)

        db.session.commit()
        msg = 'Таблицы базы данных заполнены'
        app.logger.info(msg)
        click.echo(msg)
    except Exception as e:
        db.session.rollback()
        click.echo(f'Произошла ошибка при заполнении базы данных. {e}')
