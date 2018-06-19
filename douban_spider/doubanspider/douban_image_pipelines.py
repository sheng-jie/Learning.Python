import os

import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class DoubanImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url, meta={'item': item})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        # os.rename('books/' + image_paths[0], 'books/full/' + item['name'] + '.jpg')
        return item

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        file_format = request.url.split('.')[-1]

        filename = u'full/{0[name]}.{1}'.format(item, file_format)
        return filename
