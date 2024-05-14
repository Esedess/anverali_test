import json

import requests

from . import Config, app
from .constants import FAILED_TO_UPDATE_IN_BITRIX24, UNABLE_TO_RETRIEVE_FROM_BITRIX24
from .models import Names_Man, Names_Woman


def b24rest_request(url_webhook: str, method: str, parametr: dict) -> dict:
    """
    Отправляет REST-запрос в Битрикс24.

    Args:
        url_webhook (str): URL вебхука для подключения к Битрикс24.
        method (str): Метод API Битрикс24 для вызова.
        parametr (dict): Параметры запроса.

    Returns:
        dict: Ответ от Битрикс24 в формате JSON. Если произошла ошибка, возвращает пустой словарь.
    """
    url = f'{url_webhook}{method}.json'
    try:
        response = requests.post(url, json=parametr, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        app.logger.warning({'Произошла ошибка при отправке запроса': {e}})
        return {}


def determine_gender_by_name(name):
    """
    Определяет пол по имени.

    Args:
        name (str): Имя для определения пола.

    Returns:
        str: Config.MALE, если имя мужское,
             Config.FEMALE, если имя женское,
             None, если имя не найдено.
    """
    if Names_Man.query.filter_by(name=name).first():
        return Config.MALE
    if Names_Woman.query.filter_by(name=name).first():
        return Config.FEMALE
    return None


def update_contact_genre_in_crm(contact_id: int):
    """
    Обновляет пол (genre) контакта в CRM Битрикс24 на основе его имени.

    Args:
        contact_id (int): Идентификатор контакта в Битрикс24.

    Returns:
        str: 'OK', если обновление прошло успешно,
             'Error: Unable to retrieve contact data from Bitrix24', если не удалось получить данные о контакте,
             'Error: Failed to update contact genre in Bitrix24', если не удалось обновить данные о контакте.
    """
    contact_data = b24rest_request(
        Config.WEBHOOK_URL, 'crm.contact.get', {'id': contact_id})

    if not contact_data or 'result' not in contact_data:
        app.logger.warning({'Error': UNABLE_TO_RETRIEVE_FROM_BITRIX24})
        return f'Error: {UNABLE_TO_RETRIEVE_FROM_BITRIX24}'

    result = contact_data.get('result')
    genre = result.get('HONORIFIC')
    name = result.get('NAME').lower()

    name_gender = determine_gender_by_name(name)

    if name_gender and name_gender != genre:
        update_data = {
            'id': contact_id,
            'fields': {
                Config.GENRE_FIELD: name_gender
            }
        }
        update_result = b24rest_request(
            Config.WEBHOOK_URL, 'crm.contact.update', update_data)

        if not update_result:
            app.logger.warning({'Error': FAILED_TO_UPDATE_IN_BITRIX24})
            return f'Error: {FAILED_TO_UPDATE_IN_BITRIX24}'
    if name_gender is None:
        data = {contact_id: name}
        with open('data/unknown_names.json', 'r+', encoding='utf-8') as json_file:
            file_data = json.load(json_file)
            new_data = file_data | data
            json_file.seek(0)
            json.dump(new_data, json_file, ensure_ascii=False, indent=4)
        app.logger.warning({'warning': 'Не удалось определить пол по имени'},
                           {contact_id: name})

    return 'OK'
