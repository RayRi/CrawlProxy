# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import redis
import logging
import numpy as np
import requests


class CheckBase(object):
    def __init__(self, validate_status_code=[200]):
        self.validate_code=validate_status_code

    def check(self, url, proxy):
        try:
            response = requests.get(url, proxies=proxy, timeout=10)
            print(response.json())
            if response.status_code in self.validate_code:
                return True
        except (TimeoutError, AttributeError):
            return False

class ValidateProxyMiddleware(CheckBase):
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

        super().__init__()
        
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
        result = self.check_validate(data)
        if len(result) > 0:
            # add into redis
            self.conn.sadd(dtype, *result)
        else:
            logging.info("该批次 proxies 无效")
        
    def check_validate(self, data):
        if self.single:
            result = [proxy for proxy in data if self.check(self.urls, proxy)]
        else:
            result = []
            for proxy in data:
                if all([self.check(url, proxy) for url in self.urls ]):
                    result.append(proxy)
        
        return result

class SingleValidateProxyMiddleware(object):
    """ Deal with None sequence proxies
    
    """
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
        # concatent data
        address = item["ssl"] + r"://" + item["ip"] + r":" + item["port"]

        if self.single:
            urls = [self.urls]
        else:
            urls = self.urls

        for url in urls:
            try:
                proxy = {
                    "https": address,
                    "http": address,
                }
                result = requests.get(url, proxies=proxy, timeout=10).json()
                logging.info("Value is {}".format(result))
            except:
                continue
        # if all([self.check(url, address) for url in urls ]):
        #     self.conn.sadd(item["security"], address)
        # else:
        #     logging.info("失效 proxy")

        return item