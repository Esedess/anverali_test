import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOGGING_LEVEL = os.getenv('FLASK_LOGGING_LEVEL')
    LOGFILE_PATH = os.getenv('FLASK_LOGFILE_PATH')

    WEBHOOK_URL = os.getenv('WEBHOOK_URL')
    APPLICATION_TOKEN = os.getenv('APPLICATION_TOKEN')

    GENRE_FIELD = os.getenv('GENRE_FIELD')
    MALE = os.getenv('MALE')
    FEMALE = os.getenv('FEMALE')
