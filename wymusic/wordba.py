# -*- coding: utf-8 -*-

import jieba
from wordcloud import WordCloud
from wymusic.db import new_session, Comments
import os


class Ciyun(object):

    def __init__(self):
        self.sess = new_session()
        # 写入font_path参数可以解决中文乱码问题
        self.wc = WordCloud(random_state=1, font_path=r'font.ttf')

    def to_jpg(self, song_ids):
        try:
            for i in song_ids:
                data = self.sess.query(Comments).filter_by(song_id=i).all()
                with open('comments.txt', 'w+', encoding='utf-8') as f:
                    for j in data:
                        f.write(j.content)
                text = open('comments.txt', encoding='utf-8').read()
                text_cut = jieba.cut(text)
                new_text = ' '.join(text_cut)
                self.wc.generate(new_text)
                self.wc.to_file('{}.jpg'.format(i))
                print('已生出歌曲id: %s的词云图片' % i)
        except (UnicodeEncodeError, BaseException) as e:
            print(e)
        finally:
            self.sess.close()
            os.remove('comments.txt')

    def run(self, song_ids):
        self.to_jpg(song_ids)
