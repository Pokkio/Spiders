# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery
from scrapy_codes.lianjia.lianjia.items import LianjiaItem
import time


class GzLianjiaSpider(scrapy.Spider):
    name = 'gz.lianjia'
    allowed_domains = ['gz.lianjia.com/']
    start_urls = ['http://gz.lianjia.com/zufang/rs天河']
    urls = set([])  # 存储爬取过的链接

    def parse(self, response):
        '''
        解析主页面，并获取每条信息详细页面的 url 和下一页的链接
        :param response:
        :return:
        '''
        jpy = PyQuery(response.text)
        li_list = jpy('#house-lst > li').items()  # 封装成 pyquery 对象，便于遍历
        for li in li_list:
            item = LianjiaItem()
            item['name'] = li('div.info-panel > h2 > a').text()
            addr1 = li('div.info-panel > div.col-1 > div.where > span.zone > span').text().replace('&nbsp', '')
            addr2 = li('div.info-panel > div.col-1 > div.where > span.meters').text().replace('&nbsp', '')
            addr3 = li('div.info-panel > div.col-1 > div.where > span:nth-child(4)').text()
            item['addr'] = ''.join(addr1 + addr2 + addr3)
            other1 = li('div.info-panel > div.col-1 > div.other > div > a').text()
            other2 = li('div.info-panel > div.col-1 > div.other > div').text()
            item['other'] = ''.join(other1 + other2)
            item['price'] = li('div.info-panel > div.col-3 > div.price > span').text() + '元/月'
            a = li('div.info-panel > h2 > a').attr['href']  # 详细页面链接
            self.urls.add(a)  # 存储主页面链接
            time.sleep(0.4)
            # print(a)
            yield scrapy.Request(url=a, meta={'item': item}, callback=self.parse_info, dont_filter=True)
            # yield item

        # 解析下个主页面
        for n in range(2, 4):  # 爬取2、3页
            time.sleep(0.4)
            # print(n)
            url = 'http://gz.lianjia.com/zufang/pg' + str(n) + 'rs天河/'
            self.urls.add(url)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)  # 停用过滤功能

    def parse_info(self, response):
        '''
        解析详细页面
        :param response:
        :return:
        '''
        item = response.meta['item']
        jpy = PyQuery(response.text)
        div_tag = jpy('#introduction > div > div.introContent')
        item['lease'] = div_tag('div.base > div.content > ul > li:nth-child(1)').text()
        item['payment'] = div_tag('div.base > div.content > ul > li:nth-child(2)').text()
        item['housepr'] = div_tag('div.base > div.content > ul > li:nth-child(3)').text()
        item['period'] = div_tag('div.base > div.content > ul > li:nth-child(4)').text()
        yield item
