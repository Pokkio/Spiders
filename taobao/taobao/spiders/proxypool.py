from bs4 import BeautifulSoup
from multiprocessing import Process, Queue
import random
import requests
import pymongo
import time


class Proxies(object):
    """获取代理ip"""

    def __init__(self, page=1):
        self.proxies = []
        self.verify_pro = []
        self.page = page
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)'
                                      'AppleWebKit/537.36 (KHTML, like Gecko)'
                                      'Chrome/45.0.2454.101 Safari/537.36'}
        print('正在爬取西刺代理...')
        self.get_proxies()
        self.get_proxies_nn()

    def get_proxies(self):
        '''国内普通代理'''
        page = random.randint(1, 10)
        page_stop = page + self.page
        while page < page_stop:
            url = 'http://www.xicidaili.com/nt/%d' % page
            time.sleep(random.randint(0, 3))
            html = requests.get(url, headers=self.headers).content
            soup = BeautifulSoup(html, 'lxml')
            ip_list = soup.find(id='ip_list')
            for odd in ip_list.find_all(class_='odd'):
                protocol = odd.find_all('td')[5].get_text().lower() + '://'
                self.proxies.append(protocol + ':'.join([x.get_text() for x in odd.find_all('td')[1:3]]))
            page += 1

    def get_proxies_nn(self):
        '''国内高匿代理'''
        page = random.randint(1, 10)
        page_stop = page + self.page
        while page < page_stop:
            url = 'http://www.xicidaili.com/nn/%d' % page
            time.sleep(random.randint(0, 3))
            html = requests.get(url, headers=self.headers).content
            soup = BeautifulSoup(html, 'lxml')
            ip_list = soup.find(id='ip_list')
            for odd in ip_list.find_all(class_='odd'):
                protocol = odd.find_all('td')[5].get_text().lower() + '://'
                self.proxies.append(protocol + ':'.join([x.get_text() for x in odd.find_all('td')[1:3]]))
            page += 1

    def verify_proxies(self):
        # 没验证的代理
        old_queue = Queue()
        # 验证后的代理
        new_queue = Queue()
        print('验证代理中...')
        works = []
        for _ in range(10):
            works.append(Process(target=self.verify_one_proxy, args=(old_queue, new_queue)))
        for work in works:
            work.start()
        for proxy in self.proxies:
            old_queue.put(proxy)
        for work in works:
            old_queue.put(0)
        for work in works:
            work.join()
        self.proxies = []  # 清空存取没有验证的 ip 列表
        while 1:
            try:
                self.proxies.append(new_queue.get(timeout=1))
            except:
                break
        print('代理已验证完成!')

    def verify_one_proxy(self, old_queue, new_queue):
        while 1:
            proxy = old_queue.get()
            if proxy == 0:
                break
            protocol = 'https' if 'https' in proxy else 'http'
            proxies = {protocol: proxy}
            try:
                if requests.get('http://www.baidu.com', proxies=proxies, timeout=3).status_code == 200:
                    print('可使用的代理 %s' % proxy)
                    new_queue.put({'proxy': proxy, 'protocol': protocol})
            except:
                print('已失效的代理 %s' % proxy)

if __name__ == '__main__':
    a = Proxies()
    a.verify_proxies()
    proxie = a.proxies
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client.taobao
    collection = db.proxy
    collection.insert_many(proxie)
    print('代理已全部插入到数据库!')
    client.close()
