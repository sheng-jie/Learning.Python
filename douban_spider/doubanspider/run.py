# -*- coding: utf-8 -*-

from scrapy.cmdline import execute

name = 'vote_gt9_books'
cmd = 'scrapy crawl {0}'.format(name)
execute(cmd.split())