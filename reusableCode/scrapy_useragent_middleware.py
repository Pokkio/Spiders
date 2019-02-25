from random import choice


class RandomUserAgent:
    '''
    产生随机User-Agent
    '''

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spiser):
        request.headers.setdefault('User-Agent', choice(self.agents))