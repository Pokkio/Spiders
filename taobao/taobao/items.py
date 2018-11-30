# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaoItem(scrapy.Item):
    category = scrapy.Field()  # 目录号
    comment_count = scrapy.Field()  # 评论次数
    detail_url = scrapy.Field()  # 商品详细页面链接
    item_loc = scrapy.Field()  # 物品所在地
    nickname = scrapy.Field()  # 商店名称
    raw_title = scrapy.Field()  # 商品名称
    view_price = scrapy.Field()  # 商品价格
    view_sales = scrapy.Field()  # 商品销售量
