# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FreeproxyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ip = scrapy.Field()
    port = scrapy.Field(serializer=str)
    ssl = scrapy.Field() # HTTP version ,eg: http, https
    security = scrapy.Field() # anonymous or non- anonymous
    area = scrapy.Field()   # country area