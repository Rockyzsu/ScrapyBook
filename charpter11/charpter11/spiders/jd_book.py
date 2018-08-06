# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy_splash import SplashRequest


lua_script = """
function main(splash)
    splash:go(splash.args.url)
    splash:wait(2)
    splash:runjs("document.getElementsByClassName('page')[0].scrollIntoView(true)")
    splash:wait(2)
    return splash:html()
end
"""


class JDBookSpider(scrapy.Spider):
    name = "jd_book"
    allowed_domains = ["search.jd.com"]
    base_url = 'https://search.jd.com/Search?keyword=python&enc=utf-8&wq=python'

    def start_requests(self):
        # 请求第一页，无需 js 渲染
        yield Request(self.base_url, callback=self.parse_urls, dont_filter=True)

    def parse_urls(self, response):
        # 获取商品总数，计算出总页数
        total = int(response.css('span#J_resCount::text').extract_first().strip('+'))
        pageNum = total // 60 + (1 if total % 60 else 0)

        # 构造每页的 url，向 Splash 的 execute 端点发送请求
        for i in range(pageNum):
            url = '%s&page=%s' % (self.base_url, 2*i+1)
            yield SplashRequest(url, endpoint='execute', args={'lua_source': lua_script},\
                                cache_args=['lua_source'])

    def parse(self, response):
        # 获取一个页面中每本书的名字和价格
        for sel in response.css('ul.gl-warp.clearfix > li.gl-item'):
            yield {
                'name': sel.css('div.p-name').xpath('string(.//em)').extract_first(),
                'price': sel.css('div.p-price i::text').extract_first(),
            }