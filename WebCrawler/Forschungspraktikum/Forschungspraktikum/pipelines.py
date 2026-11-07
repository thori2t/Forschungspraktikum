# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
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
        rval = super().file_path(request, response, info, item=item)
        #country = item['country'] if item else 'unknown'
        domain = item['domain']
        country = domain.split('.')[-1]
        return f"{country}/{domain}/{rval.split('/')[-1]}"
