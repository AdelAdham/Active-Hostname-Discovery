import dns.resolver
from celery import shared_task
from .models import Hostname
from .message_queue import MessageQueue

Message_queue = MessageQueue()
DISCOVERED_QUEUE_NAME = "dns_record_discovered"


@shared_task
def process_reported_host(hostname, source):
    """Saves the reported hostname to the database and perform desired processing"""
    record, created = Hostname.objects.get_or_create(hostname=hostname, source=source)
    if created:
        print(
            f"New DB record created for the reported hostname: {hostname}", flush=True
        )

    try:
        answers = dns.resolver.resolve(hostname, "A")
        ip = str(answers[0])
        record.has_a_record = True
        record.ip_address = ip
        record.save()
        # creating the message to publish
        message = {"hostname": hostname, "record_type": "A", "value": ip}
        Message_queue.publish_message(message=message, queue_name=DISCOVERED_QUEUE_NAME)
    except Exception as e:
        record.has_a_record = False
        record.save()
        print(f"DNS lookup failed for {hostname}: {e}", flush=True)
