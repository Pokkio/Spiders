# -*- coding: utf-8 -*-

import scrapy
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.downloadermiddlewares.retry import RetryMiddleware, response_status_message
import random
import time


class TaobaoSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MyUserAgentMiddleware(UserAgentMiddleware):

    def __init__(self, user_agent):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agent=crawler.settings.get('MY_USER_AGENT')
        )

    def process_request(self, request, spider):
        agent = random.choice(self.user_agent)
        request.headers['User-Agent'] = agent


class ProxyMiddleware(object):

    def process_request(self, request, spider):
        import pymongo
        client = pymongo.MongoClient(host='localhost', port=27017)
        db = client.taobao
        collection = db.proxy
        print('加上代理中...')
        if request.meta.get('proxy'):
            # 如果已有代理即更换
            collection.delete_one({'proxy': request.meta['proxy']})
            request.meta['proxy'] = collection.find()[0]['proxy']
            print('已完成代理的更换..')
        else:
            request.meta['proxy'] = collection.find()[0]['proxy']
            print('已完成代理的添加..')
        client.close()


class TBaoRetryMiddleware(RetryMiddleware):

    def delete_proxy(self, proxy):
        if proxy:
            import pymongo
            client = pymongo.MongoClient(host='localhost', port=27017)
            db = client.taobao
            collection = db.proxy
            collection.delete_one({'proxy': proxy})
            print('{} 代理已删除' % proxy)
            client.close()
        else:
            print('当前并没有使用代理！')

    def process_response(self, request, response, spider):
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            self.delete_proxy(request.meta.get(['proxy'], False))
            time.sleep(random.randint(1, 3))
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) and \
         not request.meta.get('dont_retry', False):
            self.delete_proxy(request.meta.get('proxy', False))
            time.sleep(random.randint(1, 3))
            return self._retry(request, exception, spider)