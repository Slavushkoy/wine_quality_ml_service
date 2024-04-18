import pika
import uuid
from dotenv import load_dotenv
import os

load_dotenv()

# Параметры подключения
connection_params = pika.ConnectionParameters(
    host=os.getenv('RABBITMQ_HOST'),
    port=int(os.getenv('RABBITMQ_PORT')),
    virtual_host=os.getenv('RABBITMQ_VIRTUAL_HOST'),
    credentials=pika.PlainCredentials(
        username=os.getenv('RABBITMQ_USERNAME'),
        password=os.getenv('RABBITMQ_PASSWORD')
    ),
    heartbeat=30,
    blocked_connection_timeout=2
)


def send_message(message):
    response = None
    # Установка соединения
    connection = pika.BlockingConnection(connection_params)
    # Создание канала
    channel = connection.channel()
    # Имя очереди
    queue_name = 'Vine_predict'
    # Отправка сообщения
    channel.queue_declare(queue=queue_name)  # Создание очереди (если не существует)
    # Создание временной очереди для ответов
    result_queue = channel.queue_declare(queue='', exclusive=True).method.queue
    # Генерация уникального идентификатора для запроса
    correlation_id = str(uuid.uuid4())
    # Отправка сообщения
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        properties=pika.BasicProperties(reply_to=result_queue,
                                        correlation_id=correlation_id),
        body=message)

    # Функция для обработки ответа
    def on_response(ch, method, properties, body):
        if properties.correlation_id == correlation_id:
            # Дополнительная обработка ответа
            channel.basic_cancel(consumer_tag=consumer_tag)
            # Удаление очереди
            channel.queue_delete(queue=result_queue)
            # Закрытие соединения
            connection.close()
            nonlocal response
            response = body.decode('utf-8')  # Декодирование байтовой строки в обычную строку

    # Запуск ожидания ответов
    consumer_tag = channel.basic_consume(queue=result_queue, on_message_callback=on_response, auto_ack=True)
    channel.start_consuming()
    return response
