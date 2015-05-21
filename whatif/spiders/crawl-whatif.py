from scrapy.spider import BaseSpider

class WhatifSpider(BaseSpider):
    name = "whatif"
    allowed_domains = ["what-if.xkcd.com"]
    start_urls = ["http://what-if.xkcd.com/1/"]

    def parse(self, response):

