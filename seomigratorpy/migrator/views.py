from django.shortcuts import render
from .forms import MyForm
import requests
from bs4 import BeautifulSoup



def migrator(request):
    urls = []
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            old_domain = form.cleaned_data['old_domain']
            new_domain = form.cleaned_data['new_domain']
            response = requests.get(f'http://{old_domain}', headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.text, 'html.parser')
            count = 0
            for a in soup.find_all('a', href=True):
                if count >= 2:
                    break
                url = {'href': a['href']}
                if old_domain not in url['href']:
                    continue
                url['href'] = url['href'].replace(old_domain, '').replace('http://', '').replace('https://', '').replace('www.', '')
                urls.append(url)
                count += 1
            urls = list({v['href']:v for v in urls}.values())
            for url in urls:
                url_path = url['href']
                response = requests.get(f'http://{old_domain}{url_path}', headers={'User-Agent': 'Mozilla/5.0'})
                url['old_domain_http_status'] = response.status_code
                response = requests.get(f'http://{new_domain}{url_path}', headers={'User-Agent': 'Mozilla/5.0'})
                url['new_domain_http_status'] = response.status_code
    else:
        form = MyForm()
    return render(request, 'migrator.html', {'form': form, 'urls': urls})
