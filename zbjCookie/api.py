# -*- coding: utf-8 -*-

from flask import Flask, request
from zbjCookie.operatingRedis import get_single_cookie
from zbjCookie.log import Logger

app = Flask(__name__)
logger = Logger(filename='./log/api.log')


@app.route('/')
def index():
    return '<h1 align="center">Welcome to GetThisCookie</h1>'


@app.route('/cookie/random')
def cookie():
    ip = request.remote_addr
    logger.info('[api] visitor ip is %s' % ip)
    res = get_single_cookie()
    return res


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)