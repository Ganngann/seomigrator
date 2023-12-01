# seomigratorpy/migrator/models/managers/url_manager.py

from django.db import models
from migrator.models.url import Url
from urllib.parse import urlparse, urljoin
import tldextract

class UrlManager(models.Manager):

    @staticmethod
    def get_or_create_url(url, domain=''):
        """Get or create a URL."""
        # print("############### get_or_create_url: " + url)

        try:
            # print("############### try")
            full_url = UrlManager.set_url_url(url, domain)
            # print("############### start get or create: "+ full_url)
            full_url, created = Url.objects.get_or_create(url=full_url)
            # print("############### created: " + str(created))
            # print(vars(full_url))
            return full_url, created
        except Exception as e:
            # print(e)
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
        subdomain_parts = ext.subdomain.split('.')
        if len(subdomain_parts) > 1:
            return '.'.join(subdomain_parts[:-1])  # Return all but the last part as the subdomain
        else:
            return ext.subdomain
    @staticmethod
    def extract_domain(url, current_domain):
        """Extract the domain from a URL."""
        ext = tldextract.extract(url)
        subdomain_parts = ext.subdomain.split('.')
        if len(subdomain_parts) > 1:
            # Add the last part of the subdomain to the domain
            domain = subdomain_parts[-1] + '.' + ext.domain
        else:
            domain = ext.domain
        return domain + '.' + ext.suffix if ext.domain and ext.suffix else current_domain


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
        # print("###### end set url: " + full_url)
        return full_url
