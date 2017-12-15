# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json


class City58ScrapyPipeline(object):

    def open_spider(self, spider):
        self.filename = open('city58sc.json', 'wb')  # 爬取的数据以 字节 的形式写入

    def close_spider(self, spider):
        self.filename.close()

    def process_item(self, item, spider):
        jsontext = json.dumps(dict(item)) + '\n'  # 将 item 加载成 json 格式
        self.filename.write(jsontext.encode('utf-8'))
        return item  # 切记要返回 item
