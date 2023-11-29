from django.shortcuts import render
from .forms import MyForm
import requests
from bs4 import BeautifulSoup
from migrator.models import Domain, Url, Queue
import pprint
from migrator.models.managers.url_manager import UrlManager




def migrator(request):
    # colector()

    urls = []
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            old_domain = UrlManager.get_or_create_url(form.cleaned_data['old_domain'])
            old_domain.index()
            urls = Url.objects.filter(Domain_id=old_domain.Domain_id)
            number_of_urls = len(urls)
            pprint.pprint(urls)
    else:
        form = MyForm()
    return render(request, 'migrator.html', {'form': form, 'urls': urls , 'number_of_urls': number_of_urls})

def colector(request):
    print("############################################################################# colector") 
    # Récupérer les 60 premières URL de la table Queue
    queue_urls = Queue.objects.all()[:1]
    if len(queue_urls) == 0:
        return 'stop'

    # Extraire les URL
    urls = [queue_url.url_id for queue_url in queue_urls]
    for url in urls:
        # print(url.url)
        url.index()
        queue_item = Queue.objects.get(url_id=url)
        queue_item.delete()

    return render(request, 'colector.html')


