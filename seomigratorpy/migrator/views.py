# seomigratorpy/migrator/views.py

import copy
import pprint
from django.shortcuts import render
from .forms import MyForm
from migrator.models import Domain, Url, Queue
from migrator.models.managers.url_manager import UrlManager
from itertools import zip_longest
from multiprocessing import Pool


def migrator(request):
    urls = []
    new_domain_urls = []
    joined_sets = {}
    created_count = 0
    number_of_new_urls = 0
    number_of_urls = 0
    progress = 0
    number_of_urls_with_status = 0
    number_of_new_domain_urls_with_status = 0

    form = MyForm(request.GET if request.method == "GET" else None)

    if request.method == "GET" and form.is_valid():
        new_url_to_index = form.cleaned_data["new_url_to_index"]
        old_domain, created = UrlManager.get_or_create_url(
            form.cleaned_data["old_domain"]
        )
        new_domain, created = UrlManager.get_or_create_url(
            form.cleaned_data["new_domain"]
        )
        old_domain_sitemap, created = UrlManager.get_or_create_url(
            old_domain.url + "/sitemap.xml"
        )
        sitemap = old_domain_sitemap.index()
        if not sitemap == 200:
            old_domain.index()
        urls = list(
            Url.objects.filter(domain=old_domain.domain)
        )  # Convertir en liste pour éviter les requêtes multiples
        for url in urls:
            new_uri = copy.copy(url)
            new_uri.domain = new_domain.domain
            if new_domain.subdomain:
                new_uri.subdomain = new_domain.subdomain
            new_url, created = UrlManager.get_or_create_url(
                new_uri.protocol
                + "://"
                + new_uri.subdomain.name
                + "."
                + new_uri.domain.name
                + new_uri.path
            )

            new_domain_urls.append(new_url)
            if new_url is not None:
                if new_url.last_indexed is None:
                    new_url.add_to_queue()
                    new_url.save()
            if created:  # Si "created" est "True"
                created_count += 1  # Incrémenter le compteur
                if created_count > new_url_to_index:  # Si le compteur dépasse 50
                    break  # Sortir de la boucle

        number_of_urls = len(urls)
        number_of_new_urls = len(new_domain_urls)
        joined_sets = dict(zip_longest(urls, new_domain_urls))

        urls_with_status = [url for url in urls if url.http_status is not None]
        number_of_urls_with_status = len(urls_with_status)
        new_domain_urls_with_status = [
            url for url in new_domain_urls if url.http_status is not None
        ]
        number_of_new_domain_urls_with_status = len(new_domain_urls_with_status)

    if number_of_urls > 0 and number_of_new_urls > 0:
        progress = (number_of_new_urls / number_of_urls) * 100
    
    return render(
        request,
        "migrator.html",
        {
            "form": form,
            "urls": urls,
            "number_of_urls": number_of_urls,
            "number_of_new_urls": number_of_new_urls,
            "joined_sets": joined_sets,
            "progress": progress,
            "number_of_urls_with_status": number_of_urls_with_status,
            "number_of_new_domain_urls_with_status": number_of_new_domain_urls_with_status,
        },
    )


def index_url_in_queue(queue_url):
    print("############### Indexing: " + queue_url.url.url)
    queue_url.delete()
    try:
        queue_url.url.index()
    except Exception as e:
        pass
    return vars(queue_url)


def index_url(url):
    url.queue.delete()
    url.index()
    return vars(url)


from django.db.models import Q


def collector(request):
    url_to_index = request.GET.get("url_to_index")
    domain_to_index = request.GET.get(
        "domain"
    )  # Get the domain parameter from the GET request
    domain_to_index, created = UrlManager.get_or_create_url(domain_to_index)

    if url_to_index is not None:
        url_to_index = int(url_to_index)
    else:
        url_to_index = 5
    print(url_to_index)

    # If domain parameter is defined, filter the queue by domain and subdomain
    if domain_to_index is not None:
        urls_with_queue = Url.objects.filter(
            queue__isnull=False,
            domain=domain_to_index.domain,
            subdomain=domain_to_index.subdomain,
        )[:url_to_index]
        
        for url in urls_with_queue:
            print(url.url)
            index_url(url)
        indexed_urls = urls_with_queue
            

    else:
        queue_urls = Queue.objects.all()[:url_to_index]
        # Créer un pool de processus
        with Pool(processes=1) as pool:
            indexed_urls = pool.map(index_url_in_queue, queue_urls)

    return render(request, "collector.html", {"indexed_urls": indexed_urls})
