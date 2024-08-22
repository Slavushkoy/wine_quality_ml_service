# Шаг 1
object_model.py Объектная модель сервиса

# Шаг 2
Папка database - содержит данные для подключения к локальной базе данных, config для подклюения не пушится в гит

Папка models - содержит объектную модель приложения подключенную к базе данных

# Шаг 3
Папка routes содержит эндпоинты для api
api.py - REST

Папка bot_classes содержит классы используемые для телеграм-бота
bot.py - телеграм-бот

Папка screenshots для скриншотов и записей работы системы  
Папка bot содержит скриншоты работы телеграм-бота
bot.md - скриншоты работы телеграм-бота

# Шаг 4

Папка ml_service содержит реализаю работы RabbitMQ
Файл с моделью также хранится этой папке но не выгружается в гит
rmworkers.py - поднимает три воркера для обработки сообщений
send_message.py - содержит функцию для отправки и получения ответа
docker-compose.yml - использовался приложенный к лекции без изменений

Так же рамках данного домашнего задания:
1. внесены изменения в структуру классов (бизнес логика выделена в отдельные классы)
2. доработана работа телеграм бота/ апи для получения предсказаний
3. раелизована обработка вывода историии предсказаний в телеграм боте 
4. соответствующие скриншоты добавлены в файл bot.md


upd. Добавлены исправления по комментарию проверяющего в части файлов этого урока:
- connection params вынесены в файл .env,
- обновлен файл .gitignore
- удален закомментированный код с тестами (тесты будут вынесены отдельно в рамках дз урока номер 6)
- исправления касаемо файлов не относящихся к этому уроку будут исправлены при сдаче дз по уроку номер 6

# Шаг 5

Реализован Web интерфейс на Streamlit файл front.py
Скриншоты интерфейса на ходятся в screenshots/web.md

Так же рамках данного домашнего задания:
1. внесены изменения в структуру хранения файлов согласно примеру преподователя
2. изменена авторизация для бота и апи, авторизация реализована аналогично примеру преподователя

# Шаг 6

Папка tests содержит тесты для базы и апи
Папка screenshoots/test содержит результаты запуска тестов
Так же из всех файлов проекта удален комментед код для тестов


# Шаг 7

Изменена структура проекта, в корне лежит файл docker-compose
Папка фронт содержит Docker файл для запуска streamlit
Папка app содержит Docker файлы для запуска api, telegram-bot и воркеров 
Файл docker.png в папке app/screenshots/docker содержит скриншот работы запущенного docker

# Шаг 8:
Для запуска и работы системы необзодимо заполнить файл .env по шаблону .env.template
Значения указанные в файле .env.template 

RABBITMQ_HOST- хост для RABBITMQ

RABBITMQ_PORT - порт для RABBITMQ

RABBITMQ_VIRTUAL_HOST - имя хоста RABBITMQ

RABBITMQ_USERNAME - логин для RABBITMQ

RABBITMQ_PASSWORD - пароль для RABBITMQ

BOT_TOKEN - токен вашего телеграмм-бота

SECRET_KEY - секретный ключ для шифрования данных

COOKIE_NAME - имя куки сервиса

CONNECTION_URL -  URL подключение к базе данных


