# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import redis
import logging
import numpy as np

class ValidateProxyMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            settings=settings
        )
    
    def __init__(self, settings):
        """Init variable

        Get two object variable, urls that is settings config is validated 
        the proxy; single specify only one url, if true
        """
        self.urls = settings["PROXY_TEST_URLS"]
        if isinstance(self.urls, str):
            self.single = True
        elif isinstance(self.urls, list):
            self.single = False
        else:
            raise ValueError("URL is not validate")
        
        host = settings["REDIS_HOST"]
        port = settings["REDIS_PORT"]
        db = settings["REDIS_DB"]
        password=settings["REDIS_PASSWD"]
        pool = redis.ConnectionPool(
            host=host, port=port, db=db, password=password, decode_responses=True
        )
        self.conn = redis.Redis(connection_pool=pool)
        
    def process_item(self, item, spider):
        ip = np.array(item.get("ip"))
        port = np.array(item.get("port"))
        ssl = np.array(item.get("ssl"))
        security = np.array(item.get("security"))
        
        # concatent data
        address = np.char.add(np.char.add(ssl, r"://" ), np.char.add(ip,  np.char.add(r":", port)))
        
        self.add_data(address, security, dtype="anonymous")
        self.add_data(address, security, dtype="public")

        return item

    def add_data(self, address, option, dtype="anonymous"):
        """Add specified data
        """
        data = address[np.where(option == dtype)].tolist()
        if len(data) > 0:
            # add into redis
            self.conn.sadd(dtype, *data)