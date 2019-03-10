# -*- coding: utf-8 -*-
import scrapy
import scrapy.core.scheduler
from urllib.parse import quote
import re
from lxml import etree


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']

    def start_requests(self):
        param_quote = {'param': quote('笔记本屏幕')}
        yield scrapy.Request('https://search.jd.com/Search?keyword={}&enc=utf-8&wq={}'.format(param_quote['param'],
                                                                                              param_quote['param']),
                             callback=self.parse_info_list,
                             headers={'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0; - +http://www.baidu.com/search/spider.html)'}, meta={'param': param_quote['param']})

    def parse_info_list(self, response):
        param = response.meta['param']
        html = etree.HTML(response.text)
        goods_id_pattern = re.compile(r'data-sku=(.*) ')
        goods_id_list = re.findall(goods_id_pattern, response.text)
        goods_id_list = [i.replace(' href="javascript:;"', '').replace('"', '') for i in goods_id_list]
        goods_id_str = ','.join([str(i) for i in goods_id_list])
        goods_info = []
        for li in html.xpath('//*[@id="J_goodsList"]/ul/li'):
            good_info = dict()
            price = li.xpath('div/div[2]/strong/i/text()')[0]
            name = li.xpath('div/div[3]/a/em/text()')[0].strip().replace(' ', '')
            shop = li.xpath('div/div[5]/span/a/text()')[0]
            icons = ''
            for i in li.xpath('div/div[6]/i'):
                icons += i.xpath('text()')[0] + ' '
            good_info['price'] = price
            good_info['name'] = name
            good_info['shop'] = shop
            good_info['icons'] = icons
            goods_info.append(good_info)
        new_url = 'https://search.jd.com/s_new.php?keyword={}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq={}&page=2&s=28&scrolling=y&log_id=1551277716.92793&tpl=1_M&show_items={}'.format(param, param, goods_id_str)
        yield scrapy.Request(new_url, callback=self.parse_detail,
                             headers={'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0; - +http://www.baidu.com/search/spider.html)'}, meta={'data': goods_info, 'id': goods_id_list})

    def parse_detail(self, response):
        data = response.meta['data']
        goods_old_id_list = response.meta['id']
        html = etree.HTML(response.text)
        goods_id_pattern = re.compile(r'data-sku=(.*) ')
        goods_id_list = re.findall(goods_id_pattern, response.text)
        goods_id_list = [i.replace(' href="javascript:;"', '').replace('"', '') for i in goods_id_list]
        print(goods_old_id_list, 1)
        print(goods_id_list, 2)