from django.db import models


class Hostname(models.Model):
    """Stores each reported hostname, its source, whether it has an A record, and the IP if found"""

    # unique=Ture prevents duplicates in DB and index this field for faster processing in case of scaling
    hostname = models.CharField(max_length=255, unique=True)
    source = models.CharField(max_length=100)
    has_a_record = models.BooleanField(default=False)
    ip_address = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
