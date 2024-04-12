import pika
import threading
import json
from joblib import load
import pandas as pd
import sys

from pydantic import ValidationError

sys.path.append(r'C:\Users\slavu\Start_ML\4. MLService\ml_service')
from models.schema import VineInput

# Загрузка модели
model = load("./model")

# Параметры подключения
connection_params = pika.ConnectionParameters(
    host='localhost',  # Замените на адрес вашего RabbitMQ сервера
    port=5672,  # Порт по умолчанию для RabbitMQ
    virtual_host='/',  # Виртуальный хост (обычно '/')
    credentials=pika.PlainCredentials(
        username='rmuser',  # Имя пользователя по умолчанию
        password='rmpassword'  # Пароль по умолчанию
    ),
    heartbeat=30,
    blocked_connection_timeout=2
)


# Валидация входных данных
def handler1(ch, method, properties, body):
    try:
        data_str = body.decode('utf-8')
        data_dict = json.loads(data_str)
        vine_input = VineInput(**data_dict)
        # Если данные прошли валидацию, продолжаем обработку
        handler2(ch, method, properties, vine_input)
    except ValidationError as e:
        # Если данные не прошли валидацию, обработка прерывается
        response = f"Invalid data: {e}"
        correlation_id = properties.correlation_id
        ch.basic_publish(
            exchange='',
            routing_key=reply_to,
            properties=pika.BasicProperties(correlation_id=correlation_id),
            body=response
        )


# Предсказание
def handler2(ch, method, properties, vine_input):
    vine_input_dict = vine_input.dict()
    vine_input_df = pd.DataFrame(vine_input_dict, index=[0])
    quality = model.predict(vine_input_df)[0]
    handler3(ch, method, properties, quality)


# Запись результата
def handler3(ch, method, properties, quality):
    correlation_id = properties.correlation_id
    reply_to = properties.reply_to
    quality_str = str(quality)

    ch.basic_publish(
        exchange='',
        routing_key=reply_to,
        properties=pika.BasicProperties(correlation_id=correlation_id),
        body=quality_str
    )

    print("Ответ отправлен во временную очередь")


def callback(ch, method, properties, body):
    handler1(ch, method, properties, body)


def worker():
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    channel.queue_declare(queue='Vine_predict')
    channel.basic_consume(queue='Vine_predict', on_message_callback=callback, auto_ack=True)
    print("Worker started")
    channel.start_consuming()


# Создаем несколько воркеров
for i in range(3):
    threading.Thread(target=worker).start()
