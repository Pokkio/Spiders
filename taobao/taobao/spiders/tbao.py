# -*- coding: utf-8 -*-
import scrapy
import logging
import json
from Spiders.taobao.taobao.items import TaobaoItem
from scrapy.conf import settings

logger = logging.getLogger(__name__)


class TbaoSpider(scrapy.Spider):
    name = 'tbao'
    allowed_domains = ['taobao.com']
    # 爬取搜索 男生鞋子 关键字第一页数据
    # q: 搜索关键字 data-value: 页码 ajax: 返回接口 callback: 数据格式

    def start_requests(self):
        yield scrapy.FormRequest(
            url='http://s.taobao.com/search',
            formdata={
                's': '45',  # 44*page_number + 1
                'ajax': 'true',
                'q': '男生鞋子',
            },
            cookies=settings['COOKIES']  # cookies失效快，可考虑购买账户构建cookies池
        )

    def parse(self, response):
        logger.info('Parse function called on %s' % response.url)
        item = TaobaoItem()
        # res_json = json.loads(response.body)
        print(response)
        # for data in res_json[0]['mods']['itemlist']['data']['auctions']:
        #     item['category'] = data['category']
        #     item['comment_count'] = data['comment_count']
        #     item['detail_url'] = data['detail_url']
        #     item['item_loc'] = data['item_loc']
        #     item['nickname'] = data['nick']
        #     item['raw_title'] = data['raw_title']
        #     item['view_price'] = data['view_price']
        #     item['view_sales'] = data['view_sales']
        #     yield item