# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class WhatifPipeline(object):
    def process_item(self, item, spider):
        with open(item["No"] + "-" + item["title"], "w") as f:
            print "Saving main content: {} - {}".format(item["No"], item["title"])
            f.write(item["article"])
        return item
