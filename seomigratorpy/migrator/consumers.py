from channels.generic.websocket import AsyncWebsocketConsumer
import json
import logging
logger = logging.getLogger(__name__)


class MigratorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info('Websocket connected')
        await self.accept()

    async def disconnect(self, close_code):
        logger.info('Websocket disconnected')
        pass

async def receive(self, text_data):
    logger.info('Message received: %s', text_data)
    text_data_json = json.loads(text_data)
    old_domain = text_data_json['old_domain']
    new_domain = text_data_json['new_domain']

    old_domain_http_status = None
    new_domain_http_status = None

    # respond with hello world
    # await self.send(text_data=json.dumps({
    #     'old_domain_http_status': 'old_domain_http_status',
    #     'new_domain_http_status': 'new_domain_http_status',
    # }))

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
        url_path = url['href']
        response = requests.get(f'http://{old_domain}{url_path}', headers={'User-Agent': 'Mozilla/5.0'})
        old_domain_http_status = response.status_code
        response = requests.get(f'http://{new_domain}{url_path}', headers={'User-Agent': 'Mozilla/5.0'})
        new_domain_http_status = response.status_code
        count += 1
        await self.send(text_data=json.dumps({
            'href': url,
            'old_domain_http_status': old_domain_http_status,
            'new_domain_http_status': new_domain_http_status,
        }))