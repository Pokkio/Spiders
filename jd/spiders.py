import requests
import random
from lxml import etree


user_agent = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    "Mozilla/5.0 (compatible; Baiduspider/2.0; - +http://www.baidu.com/search/spider.html)",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
]

cookies = {'xtest': '2924.cf6b6759',
           'expires': 'Fri, 29-Mar-2019 14:28:36 GMT',
           'Max-Age': '2592000',
           'domain': 'search.jd.com'}

url = 'https://search.jd.com/Search?keyword=%E7%AC%94%E8%AE%B0%E6%9C%AC%E5%B1%8F%E5%B9%95&enc=utf-8&wq=%E7%AC%94%E8%AE%B0%E6%9C%AC%E5%B1%8F%E5%B9%95&pvid=41cfba7ae6e54dbe9ba8d11f40b793bb'

html = requests.get(url, headers={'User-Agent': random.choice(user_agent)})
html_xpath = etree.HTML(html.text.encode('ISO-8859-1').decode('utf8'))
d_li = []
for li in html_xpath.xpath('//*[@id="J_goodsList"]/ul/li'):
    d = dict()
    d['photo'] = li.xpath('//*[@id="J_goodsList"]/ul/li[1]/div/div[2]/strong/i/text()')
    d_li.append(d)
print(d_li)