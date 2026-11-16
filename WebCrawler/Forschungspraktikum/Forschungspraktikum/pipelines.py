# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from urllib.parse import urlparse
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImageException, ImagesPipeline

class ForschungspraktikumPipeline(ImagesPipeline):

    # TODO hier kann man dann das Bild mit nem AI Modell oder so analyiseren
    '''
    def is_valid_image(self, image):
        raise NotImplementedError

    def get_images(self, response, request, info, *, item=None):
        for path, image, buf in super().get_images(response, request, info, item=item):
            if(not self.is_valid_image(image)):
                raise ImageException("Image does not match criteria of FroschungspraktikumPipeline")
            yield path, image, buf
    '''
    def file_path(self, request, response=None, info=None, *, item=None):
            filename = super().file_path(request, response, info, item=item).split('/')[-1]
            host = ItemAdapter(item).get('domain') if item else None
            host = (host or urlparse(request.url).hostname or 'unknown').split(':')[0]
            tld = host.rsplit('.', 1)[-1]
            return f"{tld}/{host}/{filename}"
