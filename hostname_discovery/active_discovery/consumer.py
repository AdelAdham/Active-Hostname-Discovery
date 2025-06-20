import json
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hostname_discovery.settings")
django.setup()

from active_discovery.tasks import process_reported_host
from active_discovery.message_queue import MessageQueue


def callback(ch, method, properties, body):
    """callback function for each message received from the hostname queue"""
    try:
        data = json.loads(body)
        hostname = data["hostname"]
        source = data["source"]
        process_reported_host.delay(hostname, source)
        print(f"Processed hostname from Broker: {hostname}", flush=True)
    except Exception as e:
        print(f"Error processing Broker message: {e}", flush=True)


if __name__ == "__main__":
    Message_queue = MessageQueue()
    Message_queue.consume_messages(callback_fn=callback, queue_name="hostname")
