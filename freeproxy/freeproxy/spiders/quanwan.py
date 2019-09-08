# -*- coding: utf-8 -*-
import scrapy
from freeproxy.items import FreeproxyItem
from .spiderbase import CustomerBase

class QuanwanSpider(scrapy.Spider, CustomerBase):
    name = 'quanwan'
    allowed_domains = ['goubanjia.com']
    start_urls = ['http://goubanjia.com/']

    custom_settings = {
        "DOWNLOAD_DELAY": 0, # cancel delay
        "ITEM_PIPELINES":{
            "freeproxy.pipelines.SingleValidateProxyMiddleware": 110
        }
    }
    def __init__(self):
        super().__init__()
    def parse(self, response):
        # TODO: Test with interactvate
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        item = FreeproxyItem()
        for element in response.css("tbody > tr"):
            # address = "".join(element.xpath("./td[@class='ip']/*[contains(@style, 'display')]/text()").extract())
            item["ip"] = "".join(element.xpath("./td[@class='ip']/*[contains(@style, 'display')]/text()").extract())
            item["port"] = element.xpath("./td[@class='ip']/*[contains(@class, 'port')]/text()").extract_first()
            item["security"] = self.fix_security_type(
                element.xpath("./td[2]//text()").extract_first()
            )
            item["ssl"] = element.xpath("./td[3]//text()").extract_first()
            item["area"] = self.fix_area(
                "".join(element.xpath("./td[4]/a/text()").extract())
            )
        
            yield item