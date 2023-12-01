from django.urls import path

from . import views

urlpatterns = [
    path('', views.migrator, name='migrator'),
    path('cron', views.collector, name='collector'),
]
