# -*- coding: utf-8 -*-

import pymongo
from .items import YunqiBookListItem
import re


class YunqibookPipeline(object):

    # TODO(CLay): add function of MongoDB's cluster
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'yunqi'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(
            self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, YunqiBookListItem):
            self._process_booklist_item(item, spider)
        else:
            self._process_bookdetail_item(item, spider)
        return item

    def _process_booklist_item(self, item, spider):
        '''
        处理小说基本信息
        :param item:
        :param spider:
        :return:
        '''
        self.db.bookInfo.insert(dict(item))

    def _process_bookdetail_item(self, item, spider):
        '''
        处理小说详细信息
        :param item:
        :param spider:
        :return:
        '''
        pattern = re.compile('\d+')
        item['novelLabel'] = item['novelLabel'].strip().replace('\n', '')
        match = pattern.search(item['novelAllClick'])
        item['novelAllClick'] = match.group() \
            if match else item['novelAllClick']
        match = pattern.search(item['novelMonthClick'])
        item['novelMonthClick'] = match.group() \
            if match else item['novelMonthClick']
        match = pattern.search(item['novelWeekClick'])
        item['novelWeekClick'] = match.group() \
            if match else item['novelWeekClick']
        match = pattern.search(item['novelAllPopular'])
        item['novelAllPopular'] = match.group() \
            if match else item['novelAllPopular']
        match = pattern.search(item['novelMonthPopular'])
        item['novelMonthPopular'] = match.group() \
            if match else item['novelMonthPopular']
        match = pattern.search(item['novelWeekPopular'])
        item['novelWeekPopular'] = match.group() \
            if match else item['novelWeekPopular']
        match = pattern.search(item['novelAllComm'])
        item['novelAllComm'] = match.group() \
            if match else item['novelAllComm']
        match = pattern.search(item['novelMonthComm'])
        item['novelMonthComm'] = match.group() \
            if match else item['novelMonthComm']
        match = pattern.search(item['novelWeekComm'])
        item['novelWeekComm'] = match.group() \
            if match else item['novelWeekComm']
        self.db.bookhot.insert(dict(item))