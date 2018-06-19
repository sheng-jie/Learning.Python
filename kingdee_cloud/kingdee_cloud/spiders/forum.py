# -*- coding: utf-8 -*-
"""
抓取金蝶论坛蜘蛛
"""

import scrapy
from kingdee_cloud.items import KingdeeCloudItem
import lxml.etree
import lxml.html
import datetime
from urlparse import urljoin


class ForumSpider(scrapy.Spider):
    """
    抓取金蝶论坛
    """
    name = 'kingdee_forum'
    allowed_domains = ['club.kingdee.com']
    url = ['http://club.kingdee.com/forum.php?mod=viewthread&tid=967631']
    start_urls =['http://club.kingdee.com/forum.php?mod=forumdisplay&fid=748&filter=typeid&typeid=285']
    # start_urls = [
    #     'http://club.kingdee.com/forum.php?mod=forumdisplay&fid=748&filter=typeid&typeid=282',  #BOS平台
    #     'http://club.kingdee.com/forum.php?mod=forumdisplay&fid=748&filter=typeid&typeid=283',  #基础架构
    #     'http://club.kingdee.com/forum.php?mod=forumdisplay&fid=748&filter=typeid&typeid=284',  #财务会计
    #     'http://club.kingdee.com/forum.php?mod=forumdisplay&fid=748&filter=typeid&typeid=285',  #供应链
    #     'http://club.kingdee.com/forum.php?mod=forumdisplay&fid=748&filter=typeid&typeid=286',  #制造
    #     'http://club.kingdee.com/forum.php?mod=forumdisplay&fid=748&filter=typeid&typeid=287',  #云平台
    #     'http://club.kingdee.com/forum.php?mod=forumdisplay&fid=748&filter=typeid&typeid=299',  #用户体验
    #     'http://club.kingdee.com/forum.php?mod=forumdisplay&fid=748&filter=typeid&typeid=1029',  #安装部署
    #     'http://club.kingdee.com/forum.php?mod=forumdisplay&fid=748&filter=typeid&typeid=280',  #使用心得
    #     'http://club.kingdee.com/forum.php?mod=forumdisplay&fid=748&filter=typeid&typeid=389',  #二次开发
    #     'http://club.kingdee.com/forum.php?mod=forumdisplay&fid=748&filter=typeid&typeid=379',  #客户案例
    #     'http://club.kingdee.com/forum.php?mod=forumdisplay&fid=748&filter=typeid&typeid=390',  #售前咨询
    #     'http://club.kingdee.com/forum.php?mod=forumdisplay&fid=748&filter=typeid&typeid=490',  #电商与分销
    #     'http://club.kingdee.com/forum.php?mod=forumdisplay&fid=748&filter=typeid&typeid=940',  #管理会计
    #     'http://club.kingdee.com/forum.php?mod=forumdisplay&fid=748&filter=typeid&typeid=1007',  #预算与BI
    #     'http://club.kingdee.com/forum.php?mod=forumdisplay&fid=748&filter=typeid&typeid=1026',  #服务购买咨询
    #     'http://club.kingdee.com/forum.php?mod=forumdisplay&fid=748&filter=typeid&typeid=1082',  #条码管理
    #     'http://club.kingdee.com/forum.php?mod=forumdisplay&fid=748&filter=typeid&typeid=1112',  #管理事件
    #     'http://club.kingdee.com/forum.php?mod=forumdisplay&fid=748&filter=typeid&typeid=1160'  #PLM领域
    # ]

    def parse(self, response):

        for post in response.css("div.forum-post-item-info"):
            item = KingdeeCloudItem()
            url = post.css(
                "div.post-item-header>h3.post-item-title>a::attr('href')"
            ).extract_first()
            item['title'] = post.css(
                "div.post-item-header>h3.post-item-title>a::text"
            ).extract_first()
            item['url'] = urljoin(response.url, url)
            item['domain'] = post.css(
                "div.post-publish-info>em.bk_from>a::text").extract_first()
            item['author'] = post.css(
                "div.post-publish-info>em.publish-user>a::text").extract_first(
                )
            
            dateStr= post.css("div.post-publish-info>em.publish-time::text").extract_first()

            if dateStr is not None:                
                date = datetime.datetime.strptime(dateStr,'%Y-%m-%d')
                if(date.year==2017):
                    item['post_time'] = dateStr
                else:
                    continue

            item['read_num'] = post.css(
                "div.post-publish-info>em.read-num>a::text").extract_first()
            item['reply_num'] = post.css(
                "div.post-publish-info>em.read-num>em::text").extract_first()
            # yield item

            yield scrapy.Request(
                url=item['url'], callback=self.parse_content, meta={
                    'data': item
                })

        next_page = response.css(
            "div.page-box-wraper>div.page-box>div.pg>a.nxt::attr('href')"
        ).extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_content(self, response):
        """
        抓取帖子内容
        """
        item = response.meta.get('data')
        root = lxml.html.fromstring(response.body)

        # optionally remove tags that are not usually rendered in browsers
        # javascript, HTML/HEAD, comments, add the tag names you dont want at the end
        lxml.etree.strip_elements(root, lxml.etree.Comment, "script", "head")

        # complete text
        # content_body = root.xpath(
        #     "//div[@class='article-content box-border']/div[@class='pcb passage']/div[@class='t_fsz']"
        # )[0]
        # content = lxml.html.tostring(
        #     content_body, method="text", encoding='utf-8').replace(
        #         '\r\n', ' ').replace('\n', ' ').replace(' ', '')
        # item['content'] = content
        favorite_num = response.xpath(
            "//a[@id='k_favorite']/span/text()").extract_first()
        item['favorite_num'] = favorite_num
        yield item
