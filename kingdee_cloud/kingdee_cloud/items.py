# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KingdeeCloudItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    domain = scrapy.Field()
    author = scrapy.Field()
    url = scrapy.Field()
    post_time =scrapy.Field()
    read_num = scrapy.Field()
    reply_num = scrapy.Field()
    favorite_num =scrapy.Field()
    # content = scrapy.Field()
