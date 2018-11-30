# -*- coding: utf-8 -*-

# Scrapy settings for taobao project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'taobao'

SPIDER_MODULES = ['taobao.spiders']
NEWSPIDER_MODULE = 'taobao.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'taobao (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
# REDIRECT_ENABLED = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75    Safari/537.36',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'taobao.middlewares.TaobaoSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'taobao.middlewares.MyUserAgentMiddleware': 400,
    'taobao.middlewares.ProxyMiddleware': 401
    # 'taobao.middlewares.TaobaoDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'taobao.pipelines.TaobaoPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


MY_USER_AGENT = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"]

PROXIES = [
    'http://118.190.94.224:9001', 'http://58.53.128.83:3128', 'http://61.160.247.63:808',
]

COOKIES = {
           't': 'b9da638221eb680f455c59d7947cd4fd',  # 变化
           'cookie2': '1df793283fd0aa152692de550fca1511',
           'v': '0',
           '_tb_token_': '77ee946475e0b',  # 变化
           'cna': '6ZmHFKED6V0CAXcg2baAKJXx',  # 变化
           'thw': 'cn',
           '_m_h5_tk': '1b0a91184c3f93a992b1179b66cbb9c5_1543513389546',
           '_m_h5_tk_enc': '523bdf6edadd0e5f879a94cf70b14140',  # 变化
           'unb': '1948639799',  # 变化
           'sg': '%E6%B5%8194',
           '_l_g_': 'Ug%3D%3D',
           'skt': '8bb09139a9305158',
           'cookie1': 'VvaPCINHWhjpjc1Hcus6yDGq3jJ65DME2xivbz%2BxtVk%3D',
           'csg': '85106cc7',
           'uc3': 'vt3=F8dByR1X72cbXg4MwiY%3D&id2=UojQMQBqaXBxnw%3D%3D&nk2=G4l7bq%2FY7DY%3D&lg2=W5iHLLyFOGW7aA%3D%3D',  # 变化
           'existShop': 'MTU0MzU0ODU3Mg%3D%3D',
           'tracknick': 'xi%5Cu6CB3%5Cu540D%5Cu6D41',
           'lgc': 'xi%5Cu6CB3%5Cu540D%5Cu6D41',  # 变化
           '_cc_': 'W5iHLLyFfA%3D%3D',
           'dnk': 'xi%5Cu6CB3%5Cu540D%5Cu6D41',
           '_nk_': 'xi%5Cu6CB3%5Cu540D%5Cu6D41',
           'cookie17': 'UojQMQBqaXBxnw%3D%3D',
           'tg': '0',
           'enc': 'Pe15cfdwLAt7TosIb2raaphY34EzDsvg6CsyHO4bN4cXLgG9XoEaouGMzw6eQa1%2B1UCUwwjXOAPVuiCJSZ6w%2Bw%3D%3D',
           'mt': 'ci=-1_1',
           'uc1': "cookie15=U%2BGCWk%2F75gdr5Q%3D%3D",
           'hng': 'CN%7Czh-CN%7CCNY%7C156',
           'x': 'e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0',
           'isg': 'BLu7T0YzY8IX9Vi7LU9xW0iJSp_luM5vBNrrp614sbrRDNvuNeBbYmMCIuznLCcK'  # 变化
           }

MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DBNAME = 'tbao'
MONGODB_DOCNAME = 'info'
