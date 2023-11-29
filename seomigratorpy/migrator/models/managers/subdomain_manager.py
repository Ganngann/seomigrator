from django.db import models
from migrator.models.subdomain import Subdomain
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
import tldextract
from pprint import pprint



class SubdomainManager(models.Manager):
    def get_or_create_subdomain(self, url):
        extracted_subdomain = self.extract_subdomain(url)
        # pprint(extracted_domain)
        if extracted_subdomain == '':
            return 
        else:   
            subdomain, created = Subdomain.objects.get_or_create(name=extracted_subdomain)
            if created:
                subdomain.save()
            return subdomain

    
    def extract_subdomain(self, url):
        ext = tldextract.extract(url)
        # pprint(vars(ext))
        if ext.subdomain :
            return ext.subdomain
        else:
            return ''
        