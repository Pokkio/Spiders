# -*- coding: utf-8 -*-
'''
@Author: Clay
@Module Function: 获取微信好友信息及搜狗公众号文章
@Last Modified By: Clay
@Last Modified Time: 2018-10-22
@Last Modified Content: 添加可以使用手动输入代理
'''
import itchat
import os
from db import new_session, Proxy, Public, Article
import random
import requests
import urllib
from lxml import etree
from fake_useragent import UserAgent
import re
import time


class WeChatSogou(object):

    def __init__(self):
        self.abs_path = os.path.abspath(os.path.dirname(__file__))
        self.cookie = 'sw_uuid=6970240725; dt_ssuid=8648042874; pex=C864C03270DED3DD8A06887A372DA219231FFAC25A9D64AE09E82AED12E416AC; ssuid=17035680; IPLOC=CN4401; SUID=81A316742F20910A000000005BB426A8; SUV=1538533031927157; ld=illlllllll2bHjz7lllllVm1J$DlllllNxz0kyllllwllllllZlll5@@@@@@@@@@; ABTEST=8|1538811559|v1; weixinIndexVisited=1; SNUID=6DEF164236304E62AB9713FD36B22BA3; JSESSIONID=aaawyoZ7RLDDB-80ChIzw; sct=8'

    def get_hy(self):
        itchat.login()
        if os.path.exists(os.path.abspath(os.path.dirname(__file__)) + '\data') is not True:
            os.mkdir(os.path.abspath(os.path.dirname(__file__)) + '\data')  # 创建数据目录
        friends = itchat.get_friends(update=True)[0:]
        print('您的微信列表共有%s好友' % (len(friends) - 2))

        if friends != []:
            result = [('RemarkName', '备注'), ('NickName', '微信昵称'), ('Sex', '性别'), ('City', '城市'), ('Province', '省份'),
                      ('ContactFlag', '联系标识'), ('UserName', '用户名'), ('SnsFlag', '渠道标识'), ('Signature', '个性签名')]
            for user in friends:
                os.chdir(os.path.abspath(os.path.dirname(__file__)) + '\data')  # 切换目录
                try:
                    print('--------------------------------------')
                    print('正在获取%s的数据' % (user.get('RemarkName')))
                    os.mkdir('{}'.format(user.get('RemarkName')))
                    os.chdir('{}'.format(user.get('RemarkName')))
                except BaseException:
                    print('--------------------------------------')
                    print('正在获取%s的数据' % (user.get('NickName')))
                    os.mkdir('{}'.format(user.get('NickName')))
                    os.chdir('{}'.format(user.get('NickName')))

                img = itchat.get_head_img(userName=user["UserName"])
                try:
                    with open('{}.jpg'.format(user.get('RemarkName')), 'wb') as f:
                        f.write(img)
                except BaseException:
                    with open('{}.jpg'.format(user.get('NickName')), 'wb') as f:
                        f.write(img)

                try:
                    with open('{}.txt'.format(user.get('RemarkName')), 'a', encoding='utf8') as f:
                        f.write("-----------------------\n")
                except BaseException:
                    with open('{}.txt'.format(user.get('NickName')), 'a', encoding='utf8') as f:
                        f.write("-----------------------\n")

                try:
                    for r in result:
                        with open('{}.txt'.format(user.get('RemarkName')), 'a', encoding='utf8') as f:
                            if r[1] == '性别':
                                if int(user.get(r[0])) == 0:
                                    f.write('性别' + ":" + '未标明性别' + '\n')
                                elif int(user.get(r[0])) == 1:
                                    f.write('性别' + ":" + '男生' + '\n')
                                else:
                                    f.write('性别' + ":" + '女生' + '\n')
                            else:
                                f.write(r[1] + ":" + str(user.get(r[0])) + '\n')
                    print('已获取完成%s的数据' % user.get('RemarkName'))
                    print('--------------------------------------')
                except BaseException:
                    for r in result:
                        with open('{}.txt'.format(user.get('NickName')), 'a', encoding='utf8') as f:
                            if r[1] == '性别':
                                if int(user.get(r[0])) == 0:
                                    f.write('性别' + ":" + '未标明性别' + '\n')
                                elif int(user.get(r[0])) == 1:
                                    f.write('性别' + ":" + '男生' + '\n')
                                else:
                                    f.write('性别' + ":" + '女生' + '\n')
                            else:
                                f.write(r[1] + ":" + str(user.get(r[0])) + '\n')
                    print('已获取完成%s的数据' % user.get('NickName'))
                    print('--------------------------------------')

            print('成功获取全部好友信息！')
        else:
            print('获取好友信息失败！')
            print('error1：请确保该微信号有好友！\nerror2：若该微信号有好友，那么此微信号已不允许登录网页微信！')

    def get_gzh(self, names=None, iproxy=None):
        '''通过搜狗获取微信公众号'''
        dbs = new_session()
        ua = UserAgent()
        using_proxy = {}
        headers = {'User-Agent': ua.random, 'Cookie': self.cookie, 'Referer': 'https://weixin.sogou.com/'}
        if iproxy is not None or iproxy != '':
            proxy1 = {'https': iproxy}
            proxy2 = {'http': iproxy}
            if requests.get('https://www.baidu.com', proxies=proxy1, timeout=4).status_code == 200:
                using_proxy = proxy1
            elif requests.get('https://www.baidu.com', proxies=proxy2, timeout=4).status_code == 200:
                using_proxy = proxy2
            else:
                print('手动输入的IP地址测试为无效！采用数据库代理')
                proxies = dbs.query(Proxy).all()
                proxy = random.choice(proxies)
                using_proxy = {'{}'.format(proxy.protocol): '{}:{}'.format(proxy.address, proxy.port)}

        for name in names:
            try:
                html = requests.get('https://weixin.sogou.com/weixin?type=1&s_from=input&query={}'
                                    .format(urllib.parse.quote(name)),
                                    headers=headers, timeout=4, proxies=using_proxy).text
                result = etree.HTML(html)
                public_name = result.xpath('//*[@id="sogou_vr_11002301_box_0"]/div/div[2]/p[1]/a/em/text()')[0]
                if public_name != name:
                    print('在搜狗平台搜索不到此公众号%s' % name)
                    continue
                else:
                    public_name = result.xpath('//*[@id="sogou_vr_11002301_box_0"]/div/div[2]/p[1]/a/em/text()')[0] if result.xpath('//*[@id="sogou_vr_11002301_box_0"]/div/div[2]/p[1]/a/em/text()') != [] else ''
                    function_text = ''.join(result.xpath('//*[@id="sogou_vr_11002301_box_0"]/dl[1]/dd/text()')) if result.xpath('//*[@id="sogou_vr_11002301_box_0"]/dl[1]/dd/text()') != [] else ''
                    certification = result.xpath('//*[@id="sogou_vr_11002301_box_0"]/dl[2]/dd/text()')[0] if result.xpath('//*[@id="sogou_vr_11002301_box_0"]/dl[2]/dd/text()') != [] else ''
                    recent_article = ''.join(result.xpath('//*[@id="sogou_vr_11002301_box_0"]/dl[3]/dd/a/text()')) if result.xpath('//*[@id="sogou_vr_11002301_box_0"]/dl[3]/dd/a/text()') != [] else ''
                    articles_link = result.xpath('//*[@id="sogou_vr_11002301_box_0"]/div/div[2]/p[1]/a/@href')[0]
                    public_data = {'public_name': public_name,
                                   'function': function_text,
                                   'certification': certification,
                                   'recent_article': recent_article}
                    dbs.bulk_insert_mappings(Public, public_data)

                    headers2 = {'Referer': 'https://weixin.sogou.com/weixin?type=1&s_from=input&query={}'
                                    .format(urllib.parse.quote(name)), 'User-Agent': ua.random, 'Cookie': self.cookie}
                    html2 = requests.get(articles_link, headers=headers2, timeout=4, proxies=using_proxy).text
                    result2 = etree.HTML(html2)
                    js_text = result2.xpath('/html/body/script[8]/text()')
                    pattern = re.compile(r'("content_url"\:"\S*")')
                    js_result = re.findall(pattern, js_text[0])[0]
                    headers3 = {'User-Agent': ua.random, 'Cookie': self.cookie}

                    for i in js_result:
                        k = [j for j in i.split(',')]
                        for o in k:
                            if 'content_url' in o:
                                article_link = 'https://mp.weixin.qq.com' + o.replace('amp;', '')[15:-1]
                                html3 = requests.get(article_link, headers=headers3, timeout=4, proxies=using_proxy).text
                                time.sleep(random.randint(1, 5))
                                result3 = etree.HTML(html3)
                                # 文章节点目前有两种结构，需要进行判断
                                content = ''
                                if result3.xpath('//*[@id="js_content"]/section/section[1]/section/section/section[1]/section/section/p[1]/text()') != []:
                                    for section in result3.xpath('//*[@id="js_content"]/section/section[1]/section/section'):
                                        for p in section.xpath('section/section/section'):
                                            data = p.xpath('p/text()')[0] if p.xpath('p/text()') != [] else ''
                                            content += data
                                elif result3.xpath('//*[@id="js_content"]/p[1]/span/text()') != []:
                                    for p in result3.xpath('//*[@id="js_content"]'):
                                        for span in p.xpath('//*[@id="js_content"]/p'):
                                            data = span.xpath('span/text()')[0] if span.xpath('span/text()') != [] else ''
                                            content += data
                                article_datas = {
                                    'public_name': public_name,
                                    'article_name': result3.xpath('//*[@id="activity-name"]/text()')[0],
                                    'content': content
                                }
                                dbs.bulk_insert_mappings(Article, article_datas)
                                continue
            except TimeoutError as e:
                print('%s 代理失效，正在更换代理重新进行爬取..' % using_proxy)
                dbs.query(Proxy).filter(proxy.id).delete()
                dbs.commit()
                proxy = random.choice(proxies)
                using_proxy = '{}:{}'.format(proxy.address, proxy.port)
                continue

    def run_hy(self):
        self.get_hy()

    def run_gzh(self, names=None, iproxy=None):
        self.get_gzh(names, iproxy)
