# seomigratorpy/migrator/models/url.py

from django.db import models
from urllib.parse import urlparse
from .managers.domain_manager import DomainManager
from .managers.subdomain_manager import SubdomainManager
from .queue import Queue
import requests
from bs4 import BeautifulSoup
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

    EXCLUDED_PREFIXES = (
        'tel', 
        'mailto', 
        'javascript', 
        '#',
        'ftp',
    )
    EXCLUDED_SUFFIXES = (
        # Images
        '.jpg', 
        '.jpeg', 
        '.bmp', 
        '.webp',
        '.png', 
        '.gif', 
        '.svg',
        '.ico',

        # Audio and Video
        '.mp3',
        '.wav',
        '.mp4',
        '.avi',
        '.mov',
        '.mpeg',

        # Documents
        '.pdf', 
        '.doc', 
        '.docx', 
        '.ppt', 
        '.pptx', 
        '.txt', 
        '.xlsx', 
        '.xls', 
        '.csv', 
        '.rtf',
        '.odt',
        '.ods',

        # Archives
        '.zip', 
        '.gz', 
        '.tar', 
        '.rar', 
        '.iso',
        '.7z',

        # Programming
        '.js', 
        '.json',
        '.xml',
        '.css',
        '.py',
        '.php',
        '.java',
        '.c',
        '.cpp',
        '.h',
        '.sh',
        '.swift',
        '.go',
        '.rb',

        # Databases
        '.sql',
        '.db',
        '.dbf',
        '.mdb',

        # Other
        '.log',
        '.bin',
        '.dat',
        '.bak',
        '.tmp',
    )

    def __init__(self, *args, **kwargs):
        super(Url, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.url.startswith('http'):
            self.protocol = self.set_protocol()
            self.set_subdomain()
            self.set_domain()
            self.set_path()
            self.construct_url()
            super(Url, self).save(*args, **kwargs)

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
        try:
            response = requests.get(self.url, headers={'User-Agent': 'Mozilla/5.0'})
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête GET pour l'URL {self.url}: {e}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        for a in soup.find_all('a', href=True):
            if any(a['href'].startswith(prefix) for prefix in self.EXCLUDED_PREFIXES):
                continue
            if any(a['href'].endswith(suffix) for suffix in self.EXCLUDED_SUFFIXES):
                continue

            try:
                url, created = UrlManager.get_or_create_url(a['href'], self.Domain_id.name)
                if not url.last_indexed and url.Domain_id.name == self.Domain_id.name:
                    url.add_to_queue()
            except Url.DoesNotExist:
                pass
        
        self.http_status = response.status_code
        self.last_indexed = datetime.now()
        self.time_to_first_bite = response.elapsed.total_seconds()
        self.save()

