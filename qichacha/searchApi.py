# -*- coding: utf-8 -*-
from flask import Flask
# from qichacha.selenium_spider import Sspider  # windows
from selenium_spider import Sspider  # linux


app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Welcome to QCC API!</h1>'


@app.route('/search/<addr>', methods=['GET'])
def address(addr):
    crawl_instance = Sspider(addr)
    data = crawl_instance.run()
    return data, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
