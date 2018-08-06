# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json


class TestRandomProxySpider(scrapy.Spider):
    name = 'test_random_proxy'

    def start_requests(self):
        for _ in range(100):
            yield Request('http://httpbin.org/ip', dont_filter=True)
            yield Request('https://httpbin.org/ip', dont_filter=True)

    def parse(self, response):
        print(json.loads(response.text))