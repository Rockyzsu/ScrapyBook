# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest


class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domain = ['example.webscraping.com']
    start_urls = ['http://example.webscraping.com/places/default/user/profile']

    def parse(self, response):
        # 解析登录后下载的页面，此例中为用户个人信息页面
        keys = response.css('table label::text').re('(.+):')
        values = response.css('table td.w2p_fw::text').extract()

        yield dict(zip(keys, values))

    # ------------------------登录------------------------
    # 登录页面的 url
    login_url = 'http://example.webscraping.com/places/default/user/login'

    def start_requests(self):
        yield Request(self.login_url, callback=self.login)

    def login(self, response):
        # 登录页面的解析函数，构造 FormRequest 对象提交表单
        fd = {'email': 'liushuo@webscraping.com', 'password': '12345678'}
        yield FormRequest.from_response(response, formdata=fd, callback=self.parse_login)

    def parse_login(self, response):
        # 登录成功后，继续爬取 start_urls 中的页面
        if 'Welcome Liu' in response.text:
            yield scrapy.Request('http://example.webscraping.com/places/default/user/profile', callback=self.parse)
            # yield super().start_requests()  # Python 3 语法