# -*- coding: utf-8 -*-
'''
    @author: Clay
    @desc: 网易云音乐评论
'''

import requests
import json
from fake_useragent import UserAgent
from wymusic.db import new_session, Comments
from wymusic.params import get_params, get_encSecKey
import threadpool


class Music(object):

    def __init__(self):
        self.ua = UserAgent(verify_ssl=False)
        self.headers = {'User-Agent': self.ua.random, 'Referer': 'http://music.163.com/', 'Cookie': 'appver=1.5.0.75771;'}
        # self.dbsession = new_session()

    def get_date(self, date):
        import time
        timearray = time.localtime(int(str(date)[:-3]))
        date = time.strftime("%Y-%m-%d %H:%M:%S", timearray)
        return date

    def spider(self, ids):
        sess = new_session()
        params = get_params()
        encSecKey = get_encSecKey()
        data = {
            "params": params,
            "encSecKey": encSecKey
        }
        try:
            comments_array = []
            url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?' \
                  'csrf_token='.format(ids)
            content = requests.post(url, headers=self.headers, data=data).content
            content_json = json.loads(content)
            comments = content_json['comments']
            for comment in comments:
                date = self.get_date(date=comment['time'])
                comment_dict = {
                    'user_id': comment['user']['userId'],  # 用户ID
                    'nickname': comment['user']['nickname'],  # 用户名称
                    'content': comment['content'],  # 评论内容
                    'liked_count': comment['likedCount'],  # 点赞数
                    'song_id': ids,  # 歌曲id
                    'timed': date
                }
                comments_array.append(comment_dict)
            sess.bulk_insert_mappings(Comments, comments_array)
            sess.commit()
            print('歌曲%s：评论已全部爬取完成！' % ids)
        except (TimeoutError, BaseException, AttributeError, KeyError) as e:
            sess.rollback()
            print('爬虫中断，出现错误为 %s\n 请先确认是否id：%s正确！' % (e, ids))
        finally:
            sess.close()

    def run(self, ids):
        pool = threadpool.ThreadPool(12)
        request = threadpool.makeRequests(self.spider, ids)
        [pool.putRequest(req) for req in request]
        pool.wait()
