# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class WhatifItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    article = scrapy.Field()
    question = scrapy.Field()
    attribute = scrapy.Field()
    link = scrapy.Field()
    images = scrapy.Field()
    No = scrapy.Field()
