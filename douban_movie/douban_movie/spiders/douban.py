#
# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json
import re
# from pprint import pprint


class MoviesSpider(scrapy.Spider):
    BASE_URL = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%s&sort=recommend&page_limit=%s&page_start=%s'
    MOVIE_TAG = '豆瓣高分'
    PAGE_LIMIT = 20
    page_start = 0

    name = 'movies'
    start_urls = [BASE_URL % (MOVIE_TAG, PAGE_LIMIT, page_start)]

    def parse(self, response):
        # 使用 json 模块解析响应结果
        infos = json.loads(response.body.decode('utf-8'))

        # 迭代影片信息列表
        for movie_info in infos['subjects']:
            movie_item = {}

            # 提取“片名”和“评分”，填入 item

            # 提取影片页面 url，构造 Request 发送请求，并将 item 通过 meta 参数传递给影片页面解析函数
            yield Request(movie_info['url'], callback=self.parse_movie, meta={'_movie_item': movie_item})

        # 如果 json 结果中包含的影片数量小于请求数量，说明没有影片了，否则继续搜索
        if len(infos['subjects']) == self.PAGE_LIMIT:
            self.page_start += self.PAGE_LIMIT
            url = self.BASE_URL % (self.MOVIE_TAG, self.PAGE_LIMIT, self.page_start)
            yield Request(url)

    def parse_movie(self, response):
        # 从 meta 中提取已包含“片名”和“评分”信息的 item
        movie_item = response.meta['_movie_item']

        # 获取整个信息字符串
        info = response.css('div#info').xpath('string(.)').extract_first()

        # 提取所有字段名
        fields = [s.strip().replace(':', '') for s in response.css('div#info span.pl::text').extract()]

        # 提取所有字段的值
        values = [re.sub('\s+', '', s.strip()) for s in re.split('\s*(?:%s):\s*' % '|'.join(fields), info)][1:]

        # 将所有信息填入 item
        movie_item.update(dict(zip(fields, values)))

        yield movie_item