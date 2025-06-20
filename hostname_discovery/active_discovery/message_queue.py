import pika
import json


class MessageQueue:
    """ Central class to handle communication with message queues: connection, pulishing and consuming messages"""

    def __init__(self):
        self.connection = None

    def check_or_create_connection(self):
        """Establishes connection with the Broker if not already created"""
        if not self.connection or self.connection.is_closed:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters("localhost")
            )

    def publish_message(self, message, queue_name):
        """Publishes messages to selected queue"""
        self.check_or_create_connection()
        channel = self.connection.channel()
        channel.queue_declare(queue=queue_name)
        channel.basic_publish(
            exchange="", routing_key=queue_name, body=json.dumps(message)
        )
        print("Message published", flush=True)

    def consume_messages(self, callback_fn, queue_name):
        """Listner to consume messages from selected queue"""
        self.check_or_create_connection()
        channel = self.connection.channel()
        channel.queue_declare(queue=queue_name)
        channel.basic_consume(
            queue=queue_name, on_message_callback=callback_fn, auto_ack=True
        )
        print(
            "Broker listner -> Waiting for messages. To exit press CTRL+C", flush=True
        )
        channel.start_consuming()
