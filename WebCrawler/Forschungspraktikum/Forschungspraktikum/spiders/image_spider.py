import scrapy
from Forschungspraktikum.items import ImageItem
from urllib.parse import urlparse

class ImageSpider(scrapy.Spider):
    name = 'ImageSpider'
    start_urls = [
        'https://www.tu-chemnitz.de',
        #'https://www.thalia.de/',
        #'https://tu-freiberg.de/',
        'https://www.ensicaen.fr/',
        #'https://www.lescrous.fr/'
    ]

    def parse(self, response):
        item = ImageItem()
        urls = []
        for u in response.css('img::attr(src)').getall():
            if(not u.endswith('.svg')):
                urls.append(response.urljoin(u))
        if(len(urls) == 0):
            return
        item['image_urls'] = urls
        item['domain'] = urlparse(response.url).netloc
        #item['country'] = 'de'
        yield item

        for href in response.css("a::attr(href)").getall():
            yield scrapy.Request(response.urljoin(href), callback=self.parse)
