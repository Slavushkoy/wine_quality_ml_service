import pika
import uuid
import json

# Параметры подключения
connection_params = pika.ConnectionParameters(
    host='localhost',  # Замените на адрес вашего RabbitMQ сервера
    port=5672,          # Порт по умолчанию для RabbitMQ
    virtual_host='/',   # Виртуальный хост (обычно '/')
    credentials=pika.PlainCredentials(
        username='rmuser',  # Имя пользователя по умолчанию
        password='rmpassword'   # Пароль по умолчанию
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


# Для теста
# if __name__ == "__main__":
#     vine_input = {"fixed_acidity": 5,
#                   "volatile_acidity": 5,
#                   "citric_acid": 5,
#                   "residual_sugar": 5,
#                   "chlorides": 5,
#                   "free_sulfur_dioxide": 5,
#                   "total_sulfur_dioxide": 5,
#                   "density": 5,
#                   "pH": 5,
#                   "sulphates": 5,
#                   "alcohol": 5}
#     wine_json = json.dumps(vine_input)
#     print(send_message(wine_json))