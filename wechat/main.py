# -*- coding: utf-8 -*-
'''
@Author: Clay
@Module Function: 启动文件
@Last Modified By: Clay
@Last Modified Time: 2018-10-22
@Last Modified Content: 添加可以使用手动输入代理
'''
from spider import WeChatSogou
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
    4. 获取特定公众号
    5. 获取微信文章
    6. 删除数据库
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
        if task == 0:
            run = False
        elif task == 1:
            create_db()
        elif task == 2:
            Proxies().run()
        elif task == 3:
            while os.path.exists(os.path.abspath(os.path.dirname(__file__)) + '\data'):
                shutil.rmtree(os.path.abspath(os.path.dirname(__file__)) + '\data')
            WeChatSogou().run_hy()
        elif task == 4:
            names = input('''
            ** 请输入要爬取的公众号:（可输入多个）
            ''').strip('"')
            names = [name for name in names.split(',')]
            proxy = input('''
            ** 选择手动输入代理: (ip:port(目前只接收一个)|自动请回车)
            ''')
            WeChatSogou().run_gzh(names=names, iproxy=proxy)
        elif task == 5:
            pass
        elif task == 6:
            drop_db()
            os.remove('Proxies.db')