# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Charpter11Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    name=scrapy.Field()
    price=scrapy.Field()
    remark=scrapy.Field()
    publish=scrapy.Field()
    # shop=scrapy.Field()