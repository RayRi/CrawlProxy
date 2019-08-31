# -*- coding: utf-8 -*-
import scrapy
import logging

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import SitemapSpider
from freeproxy.items import  FreeproxyItem
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, TakeFirst, MapCompose
from freeproxy.settings import REVISE_DICT

class XiciSpider(CrawlSpider):
    name = 'xici'
    allowed_domains = ['xicidaili.com']
    start_urls = ["https://www.xicidaili.com"]

    
    rules = [
        # Extract 1st page contain proxy
        Rule(LinkExtractor(allow=(r'/[wnt]{2}/',)), callback='parse_detail'),
    ]

    def parse_detail(self, response):
        # TODO: Test with interactvate
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        loader = ItemLoader(item=FreeproxyItem(), response=response, url=self.start_urls[0])

        # for element in response.css("table tr")[1:]:
        loader.add_xpath(
            "area", "//tr/td[1]/img/@alt", MapCompose(lambda x: x.lower())
        )
        loader.add_css("ip", "table > tr > td:nth-of-type(2)::text")
        loader.add_css("port", "table > tr > td:nth-of-type(3)::text")
        loader.add_css("ssl", "table > tr > td:nth-of-type(6)::text")

        loader.add_css(
            "security","table > tr > td:nth-of-type(5)::text", 
            MapCompose(self.__fix_security)
        )
            
        items = loader.load_item()
        yield items
        # # TODO: Test with interactvate
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        next_page = self.start_urls[0] + response.xpath("//div/a[@class='next_page']/@href").extract_first()
        yield scrapy.Request(next_page, callback=self.parse_detail)
        
    def __fix_security(self, value):
        """Revise the security value

        Use dict REVISE_DICT to update the security value as English word

        Args:
            value: Security type value
        
        Returns:
            result is a english words
        """
        return REVISE_DICT[value]