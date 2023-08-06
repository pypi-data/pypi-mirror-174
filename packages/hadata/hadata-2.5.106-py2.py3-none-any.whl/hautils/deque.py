import os
import threading

from hautils.rmq import get_rmq_connection


def add_to_rmq(msg):
    app_name = os.getenv("APP_NAME", "default")
    connection = get_rmq_connection()
    channel = connection.channel()
    channel.basic_publish(exchange="deque", routing_key=app_name, body=msg)
    channel.close()


def from_mq_to_deque():
    app_name = os.getenv("APP_NAME")
    connection = get_rmq_connection()
    channel = connection.channel()
    channel.exchange_declare(exchange="deque", exchange_type="direct")
    channel.queue_declare(queue=app_name, durable=True, exclusive=False, auto_delete=False)
    channel.queue_bind(exchange="deque", queue=app_name)
    channel.basic_consume(queue=app_name, on_message_callback=add_to_deque, auto_ack=True)
    channel.start_consuming()


def add_to_deque(ch, method, properties, body):
    from hautils import ha_que
    if properties.routing_key != os.getenv("APP_NAME"):
        ha_que.append(body)


if os.getenv("APP_NAME") == "backend":
    threading.Thread(target=from_mq_to_deque).start()
    consumer = threading.Thread(target=from_mq_to_deque)
    consumer.start()
