# -*- coding: utf-8 -*-
import scrapy


class A163musicSpider(scrapy.Spider):
    name = '163music'
    allowed_domains = ['music.163']
    start_urls = ['https://music.163.com/']

    def parse(self, response):
        pass
