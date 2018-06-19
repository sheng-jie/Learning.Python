# -*- coding: utf-8 -*-
import scrapy
from doubanspider.items import DoubanspiderItem


class PrinceSpider(scrapy.Spider):
    name = 'prince'
    url = 'https://book.douban.com/subject/1084336/comments/'
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }

    def start_requests(self):
        yield scrapy.Request(
            self.url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        item = DoubanspiderItem()
        for comment in response.css('div.comment'):
            item['author'] = comment.css(
                'span.comment-info > a::text').extract_first()
            item['vote'] = comment.css(
                'span.comment-vote > span.vote-count::text').extract_first()
            item['comment'] = comment.css(
                'p.comment-content::text').extract_first()
            yield item

        next_page = response.css('li.p a.page-btn::attr("href")').extract()[-1]
        if next_page is not None:
            yield response.follow(next_page, self.parse)
