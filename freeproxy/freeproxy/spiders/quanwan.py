# -*- coding: utf-8 -*-
import scrapy


class QuanwanSpider(scrapy.Spider):
    name = 'quanwan'
    allowed_domains = ['goubanjia.com']
    start_urls = ['http://goubanjia.com/']

    def parse(self, response):
        pass
