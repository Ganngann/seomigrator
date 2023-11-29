from django.contrib import admin
from .models import Url, Page, Link, Domain, Subdomain, Queue

# Register your models here.

admin.site.register(Url)
admin.site.register(Page)
admin.site.register(Link)
admin.site.register(Domain)
admin.site.register(Subdomain)
admin.site.register(Queue)
