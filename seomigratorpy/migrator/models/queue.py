# seomigratorpy/migrator/models/queue.py
from django.db import models

class Queue(models.Model):
    id = models.AutoField(primary_key=True, default=None)
    url = models.OneToOneField(
        "Url",
        on_delete=models.CASCADE,
        related_name="queue",
    )
    created = models.DateTimeField(auto_now_add=True)
