# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()  # 房名
    addr = scrapy.Field()  # 地址
    other = scrapy.Field()  # 其它
    chanquan = scrapy.Field()  # 距地铁距离
    price = scrapy.Field()  # 价格/月
    lease = scrapy.Field()  # 租赁方式
    payment = scrapy.Field()  # 付款方式
    housepr = scrapy.Field()  # 房屋现状
    period = scrapy.Field()  # 租赁周期
    describe = scrapy.Field()  # 房屋描述
    info = scrapy.Field()  # 小区介绍
    spoint = scrapy.Field()  # 小区卖点
    mating = scrapy.Field()  # 周边配套
