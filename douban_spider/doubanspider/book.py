# encoding:utf-8
import scrapy


class BookItem(scrapy.Item):
    name = scrapy.Field()  #书名
    vote = scrapy.Field()  #评分
    vote_num = scrapy.Field()  #评分人数
    rank = scrapy.Field()  #排名
    publish_info = scrapy.Field()  #出版信息（作者、出版社、出版日期）
    author = scrapy.Field()  #出版信息（作者、出版社、出版日期）
    publisher = scrapy.Field()  #出版信息（作者、出版社、出版日期）
    publish_date = scrapy.Field()  #出版信息（作者、出版社、出版日期）
    url = scrapy.Field()  #书籍链接
    images = scrapy.Field()  #书籍图片
    image_urls =scrapy.Field()
