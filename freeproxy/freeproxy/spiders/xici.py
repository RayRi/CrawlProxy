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
        # Rule(LinkExtractor(allow=(r'/[wnt]{2}/',)), callback='parse_detail'),
        # Rule(LinkExtractor(allow=(r"/[0-9]*")), callback="parse_detail")
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
        
    def __fix_security(self, value):
        """Revise the security value

        Use dict REVISE_DICT to update the security value as English word

        Args:
            value: Security type value
        
        Returns:
            result is a english words
        """
        return REVISE_DICT[value]

        # for element in response.css("table tr")[1:]:
        #     area = element.css("td:nth-of-type(1) > img").attrib.get("alt", False)
            
        #     if area:
        #         item["area"] = area.lower()
        #     else:
        #         item["area"] = None
            
        #     item["ip"] = element.css("td:nth-of-type(2)::text").extract_first()
        #     item["port"] = element.css("td:nth-of-type(3)::text").extract_first()

        #     secure = element.css("td:nth-of-type(5)::text").extract_first()
        #     item["security_type"] = REVISE_DICT[secure]
        #     item["ssl_type"] = element.css("td:nth-of-type(6)::text").extract_first()
            
        #     yield item

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
