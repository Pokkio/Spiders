# -*- coding: utf-8 -*-
'''
    Date: 2019-4-19
    Web: https://www.qichacha.com/
    Function: 采集网站工商信息、变更记录、电话、地址等数据及测试反爬措施
    TODO: 添加对另一种页面的采集规则(https://www.qichacha.com/firm_s92e92de0f8418d901f4916a3337ab85.html)
'''

import re
from urllib.parse import urlencode
from pymongo import MongoClient


def params_encode(addr):
    params_list = []
    for page in range(2, 6):
        param = urlencode({'key': addr}) + '&ajaxflag=1&p={0}&'.format(page)
        params_list.append(param)
    return params_list


def conn_mongo(host, port, db, col):
    client = MongoClient(host=host, port=port)
    db = client[db]
    return db[col]


def get_image(img_data):
    import base64
    data = img_data
    img_path = 'D:/Work-warehouse/qichacha/captcha.jpg'
    with open(img_path, 'wb') as f:
        f.write(base64.b64decode(data))
    return img_path


def verify(html_text):
    pattern = re.compile("<script>window.location.href='(.*)';</script>")
    verify_url = re.findall(pattern, html_text)
    return verify_url
