# -*- coding: utf-8 -*-
'''
@Author: Clay
@Module Function: 启动文件
@Last Modified By: Clay
@Last Modified Time: 2018-10-14
@Last Modified Content:
'''
from spider import WeChat
import os
import shutil
from proxies import Proxies
from db import create_db, drop_db


def show_task():
    return input('''
    -------------------
    0. 退出功能
    1. 创建数据库
    2. 获取更新代理
    3. 获取好友信息
    4. 获取微信公众号文章
    5. 删除数据库
    -------------------
    ''')

if __name__ == '__main__':
    run = True
    task = 0

    while run:
        task_n = int(show_task())
        try:
            task = task_n
        except ValueError as e:
            print('请输入正确的序号')
            continue
        if task_n == 0:
            run = False
        elif task_n == 1:
            create_db()
        elif task_n == 2:
            Proxies().run()
        elif task_n == 3:
            while os.path.exists(os.path.abspath(os.path.dirname(__file__)) + '\data'):
                shutil.rmtree(os.path.abspath(os.path.dirname(__file__)) + '\data')
            WeChat().run_friend()
        elif task_n == 4:
            names = input('''
            ** 请输入要爬取的公众号:（可输入多个）
            ''').strip('"')
            names = [name for name in names.split(',')]
            WeChat().run_public(names=names)
        elif task_n == 5:
            drop_db()
            os.remove('Proxies.db')