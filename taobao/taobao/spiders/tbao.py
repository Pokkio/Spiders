# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import TaobaoItem


class TbaoSpider(scrapy.Spider):
    name = 'tbao'
    allowed_domains = ['taobao.com']
    # q: 搜索关键字 data-value: 页码 ajax: 返回接口 callback: 数据格式

    def start_requests(self):
        yield scrapy.FormRequest(
            url='https://s.taobao.com/search',
            formdata={
                'data-value': '44',  # 44*(page_number - 1)
                'ajax': 'true',
                'q': '男生鞋子'
            },
            cookies={'t': 'ebfb134ddedad899d137d5cd1497c6ef;',
                     'cna': 'MuigFK2T9WwCAXcg2HyuUydB;',
                     'cookie2': '1c260201249a06f5af400e1d560545fe;',
                     'v': '0;',
                     '_tb_token_': 'e7330f1b8b663;',
                     'thw': 'cn;',
                     'skt': '45e4aec608b0e9d0;',
                     'csg': '46c7752f;',
                     'uc3': 'vt3=F8dByRMA7egJlln%2Bpo0%3D&id2=UojQMQBqaXBxnw%3D%3D&nk2=G4l7bq%2FY7DY%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D;',
                     'existShop': 'MTU0NTcyMzcwMg%3D%3D;',
                     'tracknick': 'xi%5Cu6CB3%5Cu540D%5Cu6D41;',
                     'lgc': 'xi%5Cu6CB3%5Cu540D%5Cu6D41;',
                     '_cc_': 'W5iHLLyFfA%3D%3D;',
                     'dnk': 'xi%5Cu6CB3%5Cu540D%5Cu6D41;',
                     'tg': '0;',
                     'mt': 'ci=3_1;',
                     'enc': 'B6fBmwpcDDvnguZojncm27HyF8ZAG0oqFvNNjDUHaWQkIS2eY1W0Pr0Hol7SHVaCGS9B99SYZXYhRBPay5t8xA%3D%3D;',
                     'alitrackid': 'www.taobao.com;',
                     'lastalitrackid': 'www.taobao.com;',
                     'x': 'e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0;',
                     'swfstore': '281184;',
                     'hng': 'CN%7Czh-CN%7CCNY%7C156;',
                     'uc1': 'cookie14=UoTYM8HB9gVDQA%3D%3D&lng=zh_CN&cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D&existShop=false&cookie21=WqG3DMC9Fb5mPLIQo9kR&tag=8&cookie15=U%2BGCWk%2F75gdr5Q%3D%3D&pas=0;',             'x5sec': '7b227365617263686170703b32223a226661653330663535366234386633336166653137643735666532306335636263434a4c69692b4546454f48472b342b336e756e4d4f426f4d4d546b304f44597a4f5463354f547378227d;',
                     'JSESSIONID': 'A43FEADB6D33074D0D2528FD961661F1;',
                     'l': 'aBqDpjKOysw7Cc2XLMaYsSSuj707g9BzlqO91MwmATEhNP0D5MWzLptxP_zIRsNF2rrCu82H505jf;',
                     'isg': 'BLu7S_zvY-BIdl9vZ5iSw1nUSp_luM6WBNrrp615RLqiDN3uNeH7Y-oKIuznKCcK'}  # 可考虑购买账户构建cookies池
        )

    def parse(self, response):
        item = TaobaoItem()
        res_json = json.loads(response.text)
        for data in res_json['mods']['itemlist']['data']['auctions']:
            item['category'] = data['category']
            item['comment_count'] = data['comment_count']
            item['detail_url'] = ''.join(('https:', data['detail_url']))
            item['item_loc'] = data['item_loc']
            item['nickname'] = data['nick']
            item['raw_title'] = data['raw_title']
            item['view_price'] = data['view_price']
            item['view_sales'] = data['view_sales']
            yield item
