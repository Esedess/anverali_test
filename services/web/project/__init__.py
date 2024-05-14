from logging.config import dictConfig

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import Config

from .logger import logger_config

dictConfig(logger_config(Config.LOGGING_LEVEL, Config.LOGFILE_PATH))

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from . import api_views, cli_commands, constants, models, utils
