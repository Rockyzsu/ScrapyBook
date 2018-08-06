# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ['http://quotes.toscrape.com/js/']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, args={'images': 0, 'timeout': 3})

    def parse(self, response):
        for sel in response.css('div.quote'):
            quote = sel.css('span.text::text').extract_first()
            author = sel.css('small.author::text').extract_first()
            yield {'quote': quote, 'author': author}
        href = response.css('li.next > a::attr(href)').extract_first()
        if href:
            url = response.urljoin(href)
            yield SplashRequest(url, args={'images': 0, 'timeout': 3})