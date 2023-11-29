from django.db import models
from urllib.parse import urlparse
from .managers.domain_manager import DomainManager
from .managers.subdomain_manager import SubdomainManager
# from .managers.url_manager import UrlManager
from .queue import Queue
import requests
from bs4 import BeautifulSoup
from pprint import pprint
from datetime import datetime




class Url(models.Model):
    url = models.URLField(unique=True)
    id = models.AutoField(primary_key=True)
    Subdomain_id = models.ForeignKey('Subdomain', on_delete=models.CASCADE, null=True)
    Domain_id = models.ForeignKey('Domain', on_delete=models.CASCADE)
    path = models.CharField(max_length=255, null=True)
    Page_id = models.ForeignKey('Page', on_delete=models.CASCADE, null=True)
    http_status = models.IntegerField(null=True)
    protocol = models.CharField(max_length=255, default='https')
    first_seen = models.DateTimeField(auto_now_add=True)
    last_indexed = models.DateTimeField(null=True)
    time_to_first_bite = models.FloatField(null=True)

    def __init__(self, *args, **kwargs):
        super(Url, self).__init__(*args, **kwargs)
        self.protocol = self.set_protocol()
        self.set_subdomain()
        self.set_domain()
        self.set_path()
        self.construct_url()

    def construct_url(self):
        self.url = self.protocol + '://'
        if self.Subdomain_id:
            self.url += self.Subdomain_id.name + '.'
        if self.Domain_id:
            self.url += self.Domain_id.name
        if self.path:
            self.url += self.path

    def set_path(self):
        ext = urlparse(self.url)
        if hasattr(ext, 'path'):
            self.path = ext.path

    def save(self, *args, **kwargs):
        if self.url.startswith('http'):
            super(Url, self).save(*args, **kwargs)


    def set_protocol(self):
        ext = urlparse(self.url)
        if ext.scheme == '':
            return 'https'
        return ext.scheme

    def set_domain(self):
        self.Domain_id = DomainManager().get_or_create_domain(self.url)

    def set_subdomain(self):
        self.Subdomain_id = SubdomainManager().get_or_create_subdomain(self.url)
    
    def add_to_queue(self):
        # print("############ ADD TO QUEUE: ")
        # pprint(vars(self))
        Queue.objects.get_or_create(url_id = self)
    
    def index(self):
        from .managers.url_manager import UrlManager
        response = requests.get(self.url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        for a in soup.find_all('a', href=True):
            # if the string a staert with "tel" or "mailto"
            prefixes = ('tel', 'mailto', 'javascript', '#')
            if any(a['href'].startswith(prefix) for prefix in prefixes):
                continue
            suffixes = ('.jpg', '.png', '.gif', '.css', '.js', '.pdf', '.doc', '.docx', '.ppt', '.pptx', '.txt', '.xlsx', '.xls', '.csv')
            if any(a['href'].endswith(suffix) for suffix in suffixes):
                continue

            try:
                url = UrlManager.get_or_create_url(a['href'], self.Domain_id.name)
                # print("last indexed: " + str(url.last_indexed))
                if not url.last_indexed :
                    if url.Domain_id.name == self.Domain_id.name:
                        url.add_to_queue()
            except Url.DoesNotExist:
                pass
        print("URL INDEXED: " + self.url)
        self.http_status = response.status_code
        print("HTTP STATUS: " + str(self.http_status))
        self.last_indexed = datetime.now()
        self.time_to_first_bite = response.elapsed.total_seconds()
        print("TIME TO FIRST BITE: " + str(self.time_to_first_bite))
        self.save()

