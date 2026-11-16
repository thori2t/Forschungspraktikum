import scrapy
from Forschungspraktikum.items import ImageItem
from urllib.parse import urlparse
from time import sleep

class ImageSpider(scrapy.Spider):
    name = 'ImageSpider'

    listPath = "../../TrancoListEU/top-1m.csv"

    '''start_urls = [
        'https://www.tu-chemnitz.de',
        #'https://www.thalia.de/',
        #'https://tu-freiberg.de/',
        'https://www.ensicaen.fr/',
        #'https://www.lescrous.fr/'
    ]'''

    async def start(self):
            with open(self.listPath, "rt") as f:
                index = 0
                for x in f:
                    index += 1
                    if(index > 30000):
                        break
                    domain = x.strip().split(",")[1]
                    if(domain.endswith((".de", ".fr"))):
                        print(domain)
                        yield scrapy.Request(url="https://" + domain, callback=self.parse)

    def parse(self, response):
        item = ImageItem()
        urls = []
        for sel in response.css('img'):
            u = sel.attrib.get('src', '')
            if not u or u.startswith('data:'):
                u = sel.attrib.get('data-src') or sel.attrib.get('data-lazy-src') or ''
            if not u or u.startswith('data:') or u.lower().endswith('.svg'):
                continue
            urls.append(response.urljoin(u))
        if(len(urls) == 0):
            return
        item['image_urls'] = urls
        item['domain'] = urlparse(response.url).netloc
        #item['country'] = 'de'
        yield item

        for href in response.css("a::attr(href)").getall():
            newDomain = response.urljoin(href)
            if(newDomain.endswith((".de", ".fr"))):
                print(newDomain)
                yield scrapy.Request(newDomain, callback=self.parse)
