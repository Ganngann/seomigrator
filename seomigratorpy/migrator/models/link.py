from django.db import models

class Link(models.Model):
    id = models.AutoField(primary_key=True)
    page_id = models.ForeignKey('Page', on_delete=models.CASCADE)
    url = models.ForeignKey('Url', on_delete=models.CASCADE)
    queryParam = models.CharField(max_length=255)
    fragment = models.CharField(max_length=255)