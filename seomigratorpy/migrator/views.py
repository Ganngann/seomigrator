# seomigratorpy/migrator/views.py

import copy
import pprint
from django.shortcuts import render
from .forms import MyForm
from migrator.models import Domain, Url, Queue
from migrator.models.managers.url_manager import UrlManager
from itertools import zip_longest
from multiprocessing import Pool
from django.db import OperationalError, transaction
from time import sleep


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


def index_url_in_queue_with_retry(queue_url, max_retries=100):
    for _ in range(max_retries):
        try:
            with transaction.atomic():
                queue_url.delete()
                queue_url.url.index()
        except OperationalError:
            sleep(1)  # Attendre un peu avant de réessayer peut aider
        else:
            return vars(queue_url)  # Si aucune erreur n'est levée, sortir de la boucle
    else:
        raise OperationalError("Trop de tentatives de réessai, abandon.")


def index_url_with_retry(url, max_retries=100):
    for _ in range(max_retries):
        try:
            with transaction.atomic():
                url.index()
                if hasattr(url, 'queue'):
                    url.queue.delete()
        except OperationalError:
            sleep(1)  # Attendre un peu avant de réessayer peut aider
        else:
            return vars(url)  # Si aucune erreur n'est levée, sortir de la boucle
    else:
        raise OperationalError("Trop de tentatives de réessai, abandon.")


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

    # If domain parameter is defined, filter the queue by domain and subdomain
    if domain_to_index is not None:
        urls_with_queue = Url.objects.filter(
            queue__isnull=False,
            domain=domain_to_index.domain,
            subdomain=domain_to_index.subdomain,
        )[:url_to_index]
        
        # for url in urls_with_queue:
        #     print(url.url)
        #     index_url(url)
        with Pool(processes=1) as pool:
            indexed_urls = pool.map(index_url_with_retry, urls_with_queue)
        
        # indexed_urls = urls_with_queue
            

    else:
        queue_urls = Queue.objects.all()[:url_to_index]
        # Créer un pool de processus
        with Pool(processes=1) as pool:
            indexed_urls = pool.map(index_url_in_queue_with_retry, queue_urls)

    return render(request, "collector.html", {"indexed_urls": indexed_urls})


def index(request):
    url_ids = request.POST.getlist("url_ids[]")
    urls = Url.objects.filter(id__in=url_ids)[:5]
    for url in urls:
        # get url by id
        index_url_with_retry(url)  
    return urls

def delete(request):
    url_ids = request.POST.getlist("url_ids[]")
    urls = Url.objects.filter(id__in=url_ids)
    for url in urls:
        url.delete()
    return urls

def add_to_queue(request):
    url_ids = request.POST.getlist("url_ids[]")
    urls = Url.objects.filter(id__in=url_ids)
    for url in urls:
        url.add_to_queue()
    return urls

def ajax(request):
    print("######################## AJAX")
    pprint.pprint(vars(request))
    urls = []
    action = request.POST.get("action")
    print("############## ACTION:")
    print(action)
    ids = request.POST.getlist("url_ids[]")
    print("############## IDS:")
    print(ids)
    if action == "delete":
        urls = delete(request)
    elif action == "update":
        print("################### update")
        urls = index(request)
    elif action == "add_to_queue":
        urls = add_to_queue(request)
    return render(request, "collector.html", {"indexed_urls": urls})


