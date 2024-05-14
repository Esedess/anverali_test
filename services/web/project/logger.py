def logger_config(level='DEBUG', logfile_path='log.log'):
    """
    Создает конфигурацию логгера для использования с модулем logging.

    Аргументы:
        level (str): Уровень логирования, например, 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'.
        logfile_path (str): Путь к файлу логов.

    Возвращает:
        dict: Конфигурация логгера в формате словаря, готовая для использования с logging.config.dictConfig.

    Конфигурация включает:
        - Форматирование логов с указанием времени, уровня логирования, модуля и сообщения.
        - Обработчик для вывода логов в консоль.
        - Обработчик для записи логов в файл с ротацией файлов.
    """
    return {
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
                'formatter': 'default',
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': logfile_path,
                'maxBytes': 1000000,
                'backupCount': 0,
                'formatter': 'default',
            },
        },
        'root': {'level': level, 'handlers': ['console', 'file']},
    }
