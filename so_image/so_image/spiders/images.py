# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json


class ImagesSpider(scrapy.Spider):
    BASE_URL = 'https://image.so.com/zj?ch=art&sn=%s&listtype=new&temp=1'
    start_index = 0

    # 限制最大下载数量，防止磁盘用量过大
    MAX_DOWNLOAD_NUM = 1000

    name = "images"
    allowed_domains = ["image.so.com"]
    start_urls = [BASE_URL % 0]

    def parse(self, response):
        # 使用 json 模块解析响应结果
        infos = json.loads(response.body.decode('utf8'))
        # 提取所有图片下载 url 到一个列表，赋给 item 的'image_urls'字段
        yield {'image_urls': [info['qhimg_url'] for info in infos['list']]}

        # 如 count 字段大于0，并且下载数量不足 MAX_DOWNLOAD_NUM，继续获取下一页图片信息
        self.start_index += infos['count']
        if infos['count'] > 0 and self.start_index < self.MAX_DOWNLOAD_NUM:
            yield Request(self.BASE_URL % self.start_index)