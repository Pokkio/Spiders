from scrapy.http import Request
from scrapy.utils.url import canonicalize_url


class UrlCanonicalizerMiddleware:
    '''
    规范URL
    '''

    def process_spider_output(self, response, result, spider):
        for r in result:
            if isinstance(r, Request):
                curl = canonicalize_url(Request.url)
                if curl != Request.url:
                    r = r.replace(url=curl)
            yield r