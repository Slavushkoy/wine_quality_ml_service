# Урок 1
object_model.py Объектная модель сервиса

# Урок 2
Папка database - содержит данные для подключения к локальной базе данных, config для подклюения не пушится в гит

Папка models - содержит объектную модель приложения подключенную к базе данных

# Урок 3
Папка routes содержит эндпоинты для api
api.py - REST

Папка bot_classes содержит классы используемые для телеграм-бота
bot.py - телеграм-бот

Папка screenshots для скриншотов и записей работы системы  
Папка bot содержит скриншоты работы телеграм-бота
bot.md - скриншоты работы телеграм-бота

# Урок 4

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




