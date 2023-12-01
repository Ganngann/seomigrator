from django.db import models
from migrator.models.domain import Domain
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
import tldextract
from pprint import pprint



class DomainManager(models.Manager):
    # extract domain from url
    # if domain already exists, return domain
    # else create domain and return domain
    def get_or_create_domain(self, url):
        extracted_domain = self.extract_domain(url)
        if extracted_domain == '':
            return 
        else:   
            domain, created = Domain.objects.get_or_create(name=extracted_domain)
            if created:
                domain.save()
            return domain

    
    def extract_domain(self, url):
        ext = tldextract.extract(url)
        if ext.domain and ext.suffix:
            return ext.domain + '.' + ext.suffix
        else:
            return ''
        