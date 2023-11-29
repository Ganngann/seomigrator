from django.db import models

class Page(models.Model):
    id = models.AutoField(primary_key=True)
    url_id = models.ForeignKey('Url', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)