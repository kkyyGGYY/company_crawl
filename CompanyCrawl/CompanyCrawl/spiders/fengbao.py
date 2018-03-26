# -*- coding: utf-8 -*-
import scrapy


class FengbaoSpider(scrapy.Spider):
    name = 'fengbao'
    allowed_domains = ['https://www.riskstorm.com']
    start_urls = ['http://https://www.riskstorm.com/']

    def parse(self, response):
        pass
