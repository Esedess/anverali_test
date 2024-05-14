from flask import Response, jsonify, request

from . import Config, app
from .constants import (
    LOG_FILE_NOT_FOUND,
    REQUEST_FAILED_TO_UPDATE,
    REQUEST_NO_APPLICATION_TOKEN_MESSAGE,
    REQUEST_NO_DATA_MESSAGE,
    REQUEST_NO_ID_MESSAGE,
    REQUEST_UPDATE_SUCCESS,
    UNKNOWN_NAMES_FILE_NOT_FOUND,
)
from .utils import update_contact_genre_in_crm


@app.route('/webhook', methods=('POST',))
def webhook():
    """
    Обрабатывает POST-запросы от вебхука для обновления данных контакта в CRM Битрикс24.

    Принимает данные из формы, проверяет токен приложения и идентификатор контакта,
    затем обновляет пол (genre) контакта на основе его имени.

    Returns:
        JSON-ответ с сообщением об успехе или ошибке и соответствующим HTTP-статусом.
        - 200: Если обновление прошло успешно.
        - 400: Если данные отсутствуют или контактный ID не предоставлен.
        - 401: Если токен приложения недействителен.
        - 500: Если произошла ошибка при обновлении данных контакта.
    """
    data = request.form.to_dict()

    if not data:
        app.logger.warning({'data': REQUEST_NO_DATA_MESSAGE})
        return jsonify({'error': REQUEST_NO_DATA_MESSAGE}), 400

    if not data.get('auth[application_token]') == Config.APPLICATION_TOKEN:
        app.logger.warning({'application_token': REQUEST_NO_APPLICATION_TOKEN_MESSAGE})
        return jsonify({'error': REQUEST_NO_APPLICATION_TOKEN_MESSAGE}), 401

    contact_id = data.get('data[FIELDS][ID]')
    if not contact_id:
        app.logger.warning({'id': REQUEST_NO_ID_MESSAGE})
        return jsonify({'error': REQUEST_NO_ID_MESSAGE}), 400

    try:
        update_result = update_contact_genre_in_crm(contact_id)
        if update_result != 'OK':
            app.logger.warning({'update_result': REQUEST_FAILED_TO_UPDATE})
            return jsonify({'error': REQUEST_FAILED_TO_UPDATE}), 500

        return jsonify({'message': REQUEST_UPDATE_SUCCESS}), 200

    except Exception as e:
        app.logger.warning({'error': str(e)})
        return jsonify({'error': str(e)}), 500


@app.route('/warnings', methods=('GET',))
def get_warnings():
    """
    Возвращает содержимое файла логов flusk.log.

    Этот маршрут обрабатывает GET-запросы и возвращает содержимое файла логов в виде текстового ответа.
    Если файл логов не найден, возвращается JSON-ответ с сообщением об ошибке и статусом 404.
    В случае других ошибок возвращается JSON-ответ с сообщением об ошибке и статусом 500.

    Returns:
        Response: Текстовый ответ с содержимым файла логов.
        jsonify: JSON-ответ с сообщением об ошибке и соответствующим HTTP-статусом.
    """
    try:
        with open(Config.LOGFILE_PATH, 'r') as log_file:
            log_content = log_file.read()
        return Response(log_content, mimetype='text/plain')
    except FileNotFoundError:
        app.logger.warning({'error': LOG_FILE_NOT_FOUND})
        return jsonify({'error': LOG_FILE_NOT_FOUND}), 404
    except Exception as e:
        app.logger.warning({'error': str(e)})
        return jsonify({'error': str(e)}), 500


@app.route('/unknown_names', methods=('GET',))
def get_unknown_names():
    """
    Возвращает список неизвестных имен из файла 'unknown_names.json'.

    Returns:
        Response: Ответ с содержимым файла 'unknown_names.json' в виде текста
                  с MIME-типом 'text/plain'.
        JSON: Ответ с сообщением об ошибке в формате JSON и кодом статуса 404, если файл не найден.
        JSON: Ответ с сообщением об ошибке в формате JSON и кодом статуса 500, если произошла другая ошибка.
    """
    try:
        with open('data/unknown_names.json', 'r') as file:
            unknown_names = file.read()
        return Response(unknown_names, mimetype='text/plain')
    except FileNotFoundError:
        app.logger.warning({'error': UNKNOWN_NAMES_FILE_NOT_FOUND})
        return jsonify({'error': UNKNOWN_NAMES_FILE_NOT_FOUND}), 404
    except Exception as e:
        app.logger.warning({'error': str(e)})
        return jsonify({'error': str(e)}), 500
