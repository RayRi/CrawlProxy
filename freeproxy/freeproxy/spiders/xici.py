# -*- coding: utf-8 -*-
import scrapy
import logging

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import SitemapSpider
from freeproxy.items import  FreeproxyItem
from scrapy.http import Request

class XiciSpider(CrawlSpider):
    name = 'xici'
    allowed_domains = ['xicidaili.com']
    start_urls = ["https://www.xicidaili.com"]

    
    rules = [
        # Extract 1st page contain proxy
        Rule(LinkExtractor(allow=(r'/[wnt]{2}/',)), callback='parse_detail'),
        # Rule(LinkExtractor(allow=(r"/[0-9]*")), callback="parse_detail")
    ]

    def parse_detail(self, response):
        # TODO: Test with interactvate
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        item = FreeproxyItem()
        item["proxy"] = response.url
        yield item

    # def parse(self, response):
    #     # TODO: Test with interactvate
    #     # from scrapy.shell import inspect_response
    #     # inspect_response(response, self)
    #     # pass
    #     item = FreeproxyItem()
    #     item["proxy"] = response.url
    #     yield item

if __name__ == "__main__":
    test = XiciSpider()
    # test.test()
