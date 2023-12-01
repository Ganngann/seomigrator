# seomigratorpy/migrator/models/subdomain.py
from django.db import models

class Subdomain(models.Model):
    name = models.CharField(max_length=255, unique=True, primary_key=True)
