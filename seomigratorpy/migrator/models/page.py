# seomigratorpy/migrator/models/page.py
from django.db import models

class Page(models.Model):
    id = models.AutoField(primary_key=True)
    main_url = models.ForeignKey('Url', related_name='main_url', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)