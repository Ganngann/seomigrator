from django.db import models

class Queue(models.Model):
    url = models.OneToOneField('Url', on_delete=models.CASCADE, unique=True)
    created = models.DateTimeField(auto_now_add=True)
