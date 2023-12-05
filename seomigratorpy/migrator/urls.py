from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.migrator, name='migrator'),
    path('cron', views.collector, name='collector'),
    path('ajax', views.ajax, name='ajax'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
