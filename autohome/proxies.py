# -*- coding: utf-8 -*-
from lxml import etree
import requests
from multiprocessing import Process, Queue


class Proxy:

    def __init__(self):
        self._unverified_proxies_list = []
        self.verified_proxies_list = []
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        self.test_ip_url = 'http://www.baidu.com'

    def _get_proxy(self):
        page_num = 1
        while page_num < 5:
            try:
                url = 'https://www.kuaidaili.com/free/inha/{}/'.format(page_num)
                html = requests.get(url, self.headers, timeout=4)
                html_xpath = etree.HTML(html.text)
                for tr in html_xpath.xpath('//*[@id="list"]/table/tbody/tr'):
                    ip = tr.xpath('td[1]/text()')[0]
                    port = tr.xpath('td[2]/text()')[0]
                    protocol = tr.xpath('td[4]/text()')[0]
                    proxy = {protocol: '{}:{}'.format(ip, port)}
                    self._unverified_proxies_list.append(proxy)
                    print('Get proxy: %s' % proxy)
                page_num += 1
            except (BaseException, IndexError, TimeoutError) as e:
                print('Get proxy Error: %s' % e)
                break
        print('Finished got {} pages proxies'.format(5))

    def _verify_proxies(self):
        unv_q = Queue()   # 未验证队列
        v_q = Queue()  # 已验证代理
        print('Verify proxy start....')
        works_process = []
        for _ in range(12):
            works_process.append(Process(target=self._verify_one_proxy, args=(unv_q, v_q)))
        for work in works_process:
            work.start()
        for proxy in self._unverified_proxies_list:
            unv_q.put(proxy)
        for _ in works_process:
            unv_q.put(0)
        for work in works_process:
            work.join()
        while True:
            try:
                self.verified_proxies_list.append(v_q.get(timeout=2))
            except:
                break
        print('Proxy verification succeeded!')

    def _verify_one_proxy(self, unv_q, v_q):
        while True:
            proxy = unv_q.get()
            if proxy == 0:
                break
            try:
                if requests.get(self.test_ip_url, proxies=proxy, timeout=3).status_code == 200:
                    print('Successful verification %s' % proxy)
                    v_q.put(proxy)
            except:
                print('Verification failed %s' % proxy)

    def run_func(self):
        self._get_proxy()
        self._verify_proxies()

if __name__ == '__main__':
    proxy_instance = Proxy()
    proxy_instance.run_func()
    proxies_list = proxy_instance.verified_proxies_list
    with open('proxies.txt', 'a', encoding='utf-8') as f:
        for p in proxies_list:
            s = [' '.join((k, v)) for k, v in p.items()][0]
            f.write(s + '\n')
    print('All proxies have been written into proxies.txt!')
