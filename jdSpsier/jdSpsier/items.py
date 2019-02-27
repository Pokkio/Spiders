# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdspsierItem(scrapy.Item):
    price = scrapy.Field()  # 价格
    name = scrapy.Field()  # 商品全称
    comments = scrapy.Field()  # 商品评论数
    shop = scrapy.Field()  # 商店
    icons = scrapy.Field()  # 商品的标签
