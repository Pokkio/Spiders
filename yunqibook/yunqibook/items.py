# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YunqiBookListItem(scrapy.Item):
    '''
    存取小数的基本信息
    '''
    novelId = scrapy.Field()  # 小说id
    novelName = scrapy.Field()  # 名称
    novelLink = scrapy.Field()  # 链接
    novelAuthor = scrapy.Field()  # 作者
    novelType = scrapy.Field()  # 类型
    novelStatus = scrapy.Field()  # 状态
    novelUpdateTime = scrapy.Field()  # 更新时间
    novelWords = scrapy.Field()  # 字数
    novelImageUrl = scrapy.Field()  # 封面


class YunqiBookDetailItem(scrapy.Item):
    '''
    存储小说的详细信息
    '''
    novelId = scrapy.Field()  # id
    novelLabel = scrapy.Field()  # 标签
    novelAllClick = scrapy.Field()  # 总点击量
    novelMonthClick = scrapy.Field()  # 月点击量
    novelWeekClick = scrapy.Field()  # 周点击量
    novelAllPopular = scrapy.Field()  # 总人气
    novelMonthPopular = scrapy.Field()  # 月人气
    novelWeekPopular = scrapy.Field()  # 周人气
    novelCommentNum = scrapy.Field()  # 评论数
    novelAllComm = scrapy.Field()  # 总推荐
    novelMonthComm = scrapy.Field()  # 月推荐
    novelWeekComm = scrapy.Field()  # 周推荐
