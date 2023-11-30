# seomigratorpy/migrator/views.py

from django.shortcuts import render
from .forms import MyForm
from migrator.models import Domain, Url, Queue
from migrator.models.managers.url_manager import UrlManager
from itertools import zip_longest


def migrator(request):
    urls = []
    new_domain_urls = []
    joined_sets = {}
    created_count = 0
    number_of_new_urls = 0
    number_of_urls = 0
    form = MyForm(request.POST if request.method == "POST" else None)

    if request.method == "POST" and form.is_valid():
        new_url_to_index = form.cleaned_data["new_url_to_index"]
        old_domain, created = UrlManager.get_or_create_url(form.cleaned_data["old_domain"])
        old_domain.index()
        urls = Url.objects.filter(Domain_id=old_domain.Domain_id)
        for url in urls:
            new_uri = url.url.replace(form.cleaned_data["old_domain"], form.cleaned_data["new_domain"])
            new_url, created = UrlManager.get_or_create_url(new_uri)
            new_domain_urls.append(new_url)
            if new_url is not None:
                new_url.add_to_queue()
            if created:  # Si "created" est "True"
                created_count += 1  # Incrémenter le compteur
                if created_count > new_url_to_index:  # Si le compteur dépasse 50
                    break  # Sortir de la boucle


        number_of_urls = len(urls)
        number_of_new_urls = len(new_domain_urls)
        # joined_sets = dict(zip(urls[:number_of_urls], new_domain_urls))
        joined_sets = dict(zip_longest(urls, new_domain_urls))
    
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
            "progress": progress
        },
    )


def colector(request):
    # Récupérer les 60 premières URL de la table Queue
    queue_urls = Queue.objects.all()[:10]
    if not queue_urls:
        return 'stop'

    # Extraire les URL
    for queue_url in queue_urls:
        queue_url.url_id.index()
        queue_url.delete()

    return render(request, 'colector.html')
