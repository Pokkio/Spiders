# -*- coding: utf-8 -*-
'''
    @author: Clay
    @desc: cmd功能界面
'''

from wymusic.db import create_db, drop_db
from wymusic.spiders import Music
from wymusic.wordba import Ciyun


def show_task():
    return input('''
    ----------------------
    0. 退出
    1. 创建数据库
    2. 爬取评论
    3. 生出词云
    4. 删除数据库
    ----------------------
    ''')


if __name__ == '__main__':
    task = 0
    run = True

    while run:
        task_n = show_task()
        try:
            task = int(task_n)
        except (ValueError, TypeError) as e:
            print('请输入正确的序号！')
            continue
        if task == 0:
            run = False
        elif task == 1:
            create_db()
        elif task == 2:
            ids = input('''
            ---------------------------------------
            请输入要爬取的歌曲id（多个请以英文逗号分开）
            ---------------------------------------
            ''')
            try:
                ids_array = [int(i) for i in ids.split(',')]
            except (ValueError, TypeError) as e:
                print('请输入正确的id！')
                continue
            Music().run(ids_array)
        elif task == 3:
            ids = input('''
            ---------------------------------------
            请输入要生成词云的歌曲id（多个请以英文逗号分开）
            ---------------------------------------
                        ''')
            try:
                ids_array = [int(i) for i in ids.split(',')]
            except (ValueError, TypeError) as e:
                print('请输入正确的id！')
                continue
            Ciyun().run(ids_array)
        elif task == 4:
            drop_db()