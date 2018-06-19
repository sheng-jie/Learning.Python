# -*- coding: utf-8 -*-

from scrapy import cmdline

name = 'kingdee_forum'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())