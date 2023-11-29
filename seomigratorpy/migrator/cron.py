from .models import Queue


def url_colector():
    print("############################################################################# url_colector")

    # Récupérer les 60 premières URL de la table Queue
    queue_urls = Queue.objects.all()[:60]

    # Extraire les URL
    urls = [queue_url.url_id.url for queue_url in queue_urls]

    pass