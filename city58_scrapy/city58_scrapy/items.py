# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class City58ScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    room = scrapy.Field()
    des = scrapy.Field()  # 描述
    type = scrapy.Field()  # 房屋类型
    dire = scrapy.Field()  # 楼层朝向
