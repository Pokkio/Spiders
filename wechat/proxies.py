# -*- coding: utf-8 -*-
'''
@Author: Clay
@Module Function: 获取可用IP
@Last Modified By: Clay
@Last Modified Time: 2018-10-15
@Last Modified Content:
'''

import requests
from bs4 import BeautifulSoup
from db import new_session, Proxy
import random
import re


class Proxies(object):

    def __init__(self, page=3):
        self.dbs = new_session()
        self.page = page
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}

    def get_proxies_nn(self):
        '''获取高匿代理'''
        page = random.randint(1, 10)
        page_stop = page + self.page
        proxies = []
        pattern = re.compile(r'>(\S*)<')
        while page < page_stop:
            url = 'http://www.xicidaili.com/nn/%s' % page
            html = requests.get(url, headers=self.headers).content
            soup = BeautifulSoup(html, 'lxml')
            ip_list = soup.find(id='ip_list')
            for odd in ip_list.find_all(class_='odd'):
                protocol = odd.find_all('td')[5].get_text().lower()
                address = re.findall(pattern, str(odd.find_all('td')[1:3][0]))[0]
                port = re.findall(pattern, str(odd.find_all('td')[1:3][1]))[0]
                proxy = {
                    'address': address,
                    'protocol': protocol,
                    'port': port
                }
                proxies.append(proxy)
            page += 1
        self.dbs.bulk_insert_mappings(Proxy, proxies)
        self.dbs.commit()

    def get_proxies_wn(self):
        '''获取HTTPS代理'''
        page = random.randint(1, 10)
        page_stop = page + self.page
        proxies = []
        pattern = re.compile(r'>(\S*)<')
        while page < page_stop:
            url = 'http://www.xicidaili.com/wn/%s' % page
            html = requests.get(url, headers=self.headers).content
            soup = BeautifulSoup(html, 'lxml')
            ip_list = soup.find(id='ip_list')
            for odd in ip_list.find_all(class_='odd'):
                protocol = odd.find_all('td')[5].get_text().lower()
                address = re.findall(pattern, str(odd.find_all('td')[1:3][0]))[0]
                port = re.findall(pattern, str(odd.find_all('td')[1:3][1]))[0]
                proxy = {
                    'address': address,
                    'protocol': protocol,
                    'port': port
                }
                proxies.append(proxy)
            page += 1
        self.dbs.bulk_insert_mappings(Proxy, proxies)
        self.dbs.commit()

    def verify_proxies(self):
        proxies = self.dbs.query(Proxy).yield_per(1000)
        update_proxies = []
        for record in proxies:
            protocol = 'http' if record.protocol != 'http' else 'https'
            proxy = {protocol: record.address + ':' + record.port}
            try:
                if requests.get('https://www.baidu.com', proxies=proxy,
                                timeout=4,
                                headers={'Connection': 'close'}).status_code == 200:
                    print('already update %s' % proxy)
                    update_proxy = {
                        'id': record.id,
                        'address': record.address,
                        'protocol': record.protocol,
                        'port': record.port
                    }
                    update_proxies.append(update_proxy)
                else:
                    print('already delete %s' % proxy)
                    self.dbs.query(Proxy).filter(Proxy.id == record.id).delete()
            except BaseException as e:
                print(e)
                continue
        self.dbs.bulk_update_mappings(Proxy, update_proxies)
        self.dbs.commit()
        self.dbs.close()

    def run(self):
        self.get_proxies_nn()
        self.get_proxies_wn()
        self.verify_proxies()

