# anverali_test

Тестовое задание на обновление пола в контакте Bitrix24.

***

## Как запустить проект:


1. [Установите](https://docs.docker.com/engine/install/) docker и docker compose.

2. Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone https://github.com/Esedess/anverali_test
```
3. Создайте `.env` файл в корневой папке проекта и укажите необходимые переменные окружения, по примеру шаблона [.env_example](https://github.com/Esedess/anverali_test/.env_example).



### Локальный запуск в docker compose

1. Активируйте виртуальное окружение и установите зависимости

2. Создайте локальные папки '/www/nginx' и '/www/web'

3. Для запуска локальной версии приложения, состоящей из трех сервисов - backend (Flask приложение), postgres (БД PostgreSQL) и nginx (веб-сервер), выполните следующую команду:
    ```bash
    sudo docker-compose -f docker-compose.yml up
    ```
4. Для создания и наполнения базы выполните следующие команды:
    ```bash
    sudo docker-compose exec web flask create_db
    sudo docker-compose exec web flask seed_db
    ```

Теперь ваш сервер доступен по адресу Ваш_ip:1337.



## Endpoint'ы:

1. Ваш_ip:1337/webhook - На этот эндпоинт ваш Битрикс24 должен отправлять хук изменения контакта.

2. Ваш_ip:1337/warnings - Вывод логов

3. Ваш_ip:1337/unknown_names - Вывод имен которых нет в базе



## Настройка Битрикс24:

1. Создать исходящий вэбхук на событие "Обновление контакта (ONCRMCONTACTUPDATE)".
    В качестве URL вашего обработчика указать - http://Ваш_ip:1337/webhook
    Токен приложения добавить в .env

2. Создать входящий вебхук.
    URL для вызова rest api добавить в .env

***

## Tech Stack

+ `Python` : <https://github.com/python>
+ `Flask` : <https://github.com/pallets/flask>
+ `Flask-SQLAlchemy Extension` : <https://github.com/pallets-eco/flask-sqlalchemy>
+ `Docker` : <https://github.com/docker>
+ `Docker compose` : <https://github.com/docker/compose>
+ `nginx` : <https://github.com/nginx>

***

## Авторы

- [@Esedess](https://github.com/Esedess)