from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Définir la variable d'environnement DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seomigratorpy.settings')

app = Celery('seomigratorpy')

# Utiliser le fichier de configuration Django pour configurer Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Charger les tâches de toutes les applications enregistrées
app.autodiscover_tasks()
