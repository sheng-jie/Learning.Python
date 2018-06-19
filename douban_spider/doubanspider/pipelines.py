# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DoubanspiderPipeline(object):

    def process_item(self, item, spider):
        """
        处理出版信息，抓取作者、出版社、发版日期
        """   
        publish_info = item['publish_info']
        author = publish_info[0].split(': ')[-1]
        publisher = publish_info[1].split(': ')[-1]
        publish_date = publish_info[2].split(': ')[-1]
        item['author'] = author.strip()
        item['publisher'] = publisher.strip()
        item['publish_date'] = publish_date.strip()

        return item
