# -*- coding: utf-8 -*-
"""抓取豆瓣读书评分9分以上榜单"""

import scrapy

from doubanspider.book import BookItem


class VoteGt9BooksSpider(scrapy.Spider):
    """
    豆瓣9分榜单爬虫
    """
    name = 'vote_gt9_books'
    allowed_domains = ['www.douban.com']
    url = 'https://www.douban.com/doulist/1264675/'
    # start_urls = ['https://www.douban.com/doulist/1264675/']
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }

    custom_settings = {
        'IMAGES_STORE':
        'books',
        'FEED_FORMAT':
        'json',
        'FEED_URI':
        'book.json',
        'FEED_EXPORT_FIELDS':
        ["name", "author", "publisher", "publish_date", "vote", "rank"]
    }

    def start_requests(self):
        yield scrapy.Request(
            self.url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        for book in response.css("div.doulist-item"):
            bookitem = BookItem()
            name = book.css(
                'div.doulist-subject>div.title>a::text').extract_first()
            bookitem['name'] = name.replace('\n', '').strip()
            bookitem['vote'] = book.css(
                'div.doulist-subject>div.rating span.rating_nums::text'
            ).extract_first()
            bookitem['rank'] = book.css(
                'div.mod>div.hd>span.pos::text').extract_first()
            publish_info = book.xpath(
                './/div[@class="bd doulist-subject"]/div[@class="abstract"]/text()'
            ).extract()
            bookitem['publish_info'] = publish_info
            bookitem['url'] = book.css(
                'div.doulist-subject>div.title>a::attr("href")').extract_first(
                )
            bookitem['image_urls'] = book.css(
                'div.post img::attr("src")').extract()
            yield bookitem

        next_page = response.css(
            'div.paginator>span.next>a::attr("href")').extract_first()
        if next_page is not None:
            # yield response.follow(next_page, self.parse)
            yield scrapy.Request(
                next_page, callback=self.parse, headers=self.headers)
