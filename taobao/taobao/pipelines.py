# -*- coding: utf-8 -*-

from scrapy.exceptions import DropItem
from pymongo import MongoClient
from scrapy.conf import settings


class TaobaoPipeline(object):

    def __init__(self):
        self.host = settings.get('MONGODB_HOST')
        self.port = settings.get('MONGODB_PORT')
        self.db_name = settings.get('MONGODB_DBNAME')
        self.doc_name = settings.get('MONGODB_DOCNAME')
        self.category_seen = set()

    def open_spider(self, spider):
        self.client = MongoClient(host=self.host, port=self.port)
        db = self.client[settings['MONGODB_DBNAME']]
        self.post = db[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        try:
            if item.get('category') in self.category_seen:
                raise DropItem('Duplicate item found: %s' % item)
            else:
                self.category_seen.add(item.get('id'))
                item_dict = dict(item)
                self.post.insert(item_dict)
                return item
        except BaseException as e:
            raise e

    def close_spider(self, spider):
        self.client.close()
