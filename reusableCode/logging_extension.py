# 日志扩展
import logging
from scrapy import signals
from scrapy.exceptions import NotConfigured


logger = logging.getLogger(__name__)


class SpiderOpenCloseLogging:
    '''
    触发功能时记录日志
    '''

    def __init__(self, item_count):
        self.item_count = item_count
        self.items_scraped = 0

    @classmethod
    def from_crawler(cls, crawler):
        # 检查配置是否存在
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured
        item_count = crawler.settings.getint('MYEXT_ITEMCOUNT', 1000)
        ext = cls(item_count)
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)
        return ext

    def spider_opened(self, spider):
        logger.info('opened spider %s', spider.name)

    def spider_closed(self, spider):
        logger.info('closed spider %s', spider.name)

    def item_scraped(self, item, spider):
        self.item_scraped += 1
        if self.items_count % self.item_count == 0:
            logger.info('scraped %d items', self.items_count)