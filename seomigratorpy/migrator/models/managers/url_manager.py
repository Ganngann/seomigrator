# seomigratorpy/migrator/models/managers/url_manager.py

from django.db import models
from migrator.models.url import Url
from urllib.parse import urlparse, urljoin
import tldextract

class UrlManager(models.Manager):

    @staticmethod
    def get_or_create_url(url, domain=''):
        """Get or create a URL."""
        try:
            full_url = UrlManager.set_url_url(url, domain)
            full_url, created = Url.objects.get_or_create(url=full_url)
            if created:
                full_url.save()
            return full_url, created
        except Exception as e:
            print(f"Erreur lors de la création de l'URL {url} : {e}")
            return None, False

    @staticmethod
    def extract_protocol(url):
        """Extract the protocol from a URL."""
        ext = urlparse(url)
        return ext.scheme if ext.scheme else 'https'

    @staticmethod
    def extract_subdomain(url):
        """Extract the subdomain from a URL."""
        ext = tldextract.extract(url)
        return ext.subdomain

    @staticmethod
    def extract_domain(url, current_domain):
        """Extract the domain from a URL."""
        ext = tldextract.extract(url)
        return ext.domain + '.' + ext.suffix if ext.domain and ext.suffix else current_domain

    @staticmethod
    def extract_path(url):
        """Extract the path from a URL."""
        ext = urlparse(url)
        return ext.path if hasattr(ext, 'path') else ''

    @staticmethod
    def set_url_url(url, current_domain):
        """Set the URL."""
        protocol = UrlManager.extract_protocol(url)
        full_url = protocol + '://'
        subdomain = UrlManager.extract_subdomain(url)
        if subdomain:
            full_url += subdomain + '.'
        domain = UrlManager.extract_domain(url, current_domain)
        full_url += domain if domain else ''
        path = UrlManager.extract_path(url)
        if path == domain:
            path = ''
        full_url += path
        return full_url
