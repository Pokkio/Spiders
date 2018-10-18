# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from scrapy.conf import settings


class LianjiaPipeline(object):

    # 初始化数据库
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        db_name = settings['MONGODB_DBNAME']
        doc_name = settings['MONGODB_DOCNAME']
        self.client = MongoClient(host=host, port=port)
        db = self.client[db_name]  # 获得数据库的句柄
        self.post = db[settings['MONGODB_DOCNAME']]  # 获得 collection 句柄

    def process_item(self, item, spider):
        lianjia_info = dict(item)   # 把item转化成字典形式
        self.post.insert(lianjia_info)   # 向数据库插入一条记录
        return item  # 会在控制台输出原item数据

    def close_spider(self, spider):
        self.client.close()