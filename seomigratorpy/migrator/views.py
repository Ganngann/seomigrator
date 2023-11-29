# seomigratorpy/migrator/views.py

from django.shortcuts import render
from .forms import MyForm
from migrator.models import Domain, Url, Queue
from migrator.models.managers.url_manager import UrlManager

def migrator(request):
    number_of_urls = 0
    urls = []
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            old_domain = UrlManager.get_or_create_url(form.cleaned_data['old_domain'])
            old_domain.index()
            urls = Url.objects.filter(Domain_id=old_domain.Domain_id)
            number_of_urls = urls.count()
    else:
        form = MyForm()

    return render(request, 'migrator.html', {'form': form, 'urls': urls , 'number_of_urls': number_of_urls})

def colector(request):
    # Récupérer les 60 premières URL de la table Queue
    queue_urls = Queue.objects.all()[:60]
    if not queue_urls:
        return 'stop'

    # Extraire les URL
    for queue_url in queue_urls:
        queue_url.url_id.index()
        queue_url.delete()

    return render(request, 'colector.html')
