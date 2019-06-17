# -*- coding: utf-8 -*-
"""
    Date:
"""
import requests
from baacloudAutoLogin.baidu_ocr import Ocr
import re
from time import sleep, time
from random import randint
import sched


class AutoLogin:
    _headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }
    _email = 'xxxxx'
    _password = 'xxxxx'
    _register_url = 'http://api.cn3.me/url.php?id=2'
    _login_url = 'https://{}/modules/_login.php'
    _captcha_url = 'https://{}/other/captcha.php'
    _session = requests.session()
    _ocr = Ocr()
    _verified_number = 0

    def _get_captcha(self, domain):
        """
        获取验证码
        :param domain:
        :return:
        """
        try:
            image_data = self._session.get(self._captcha_url.format(domain), headers=self._headers).content
            code = self._ocr.run(image_data)
            captach_url = 'https://' + domain + '/modules/_checkin.php?captcha=' + code
            verified_res = self._session.get(captach_url, headers=self._headers)
        except BaseException as e:
            print('[captcha] error is %s' % e)
        else:
            res = re.findall(r'<script>alert(.*);self.location=document.referrer;</script>', verified_res.text)[0]
            while '错误' in res:
                self._verified_number += 1
                print('[verified] 已验证%d次' % self._verified_number)
                sleep(randint(1, 3))
                self._get_captcha(domain)

    def _get_domain(self):
        """
        获取更新的url
        :return:
        """
        index_url = requests.get('http://api.cn3.me/url.php?id=3')
        domain = index_url.url.split('/')[-3]
        return domain

    def _login(self):
        """
        登录
        :return:
        """
        try:
            domain = self._get_domain()
            login_url = self._login_url.format(domain)
            form_data = {
                'email': self._email,
                'passwd': self._password,
                'remember_me': 'week'
            }
            res = self._session.post(login_url, data=form_data, headers=self._headers, timeout=30)
            res.encoding = res.apparent_encoding
            res_json = res.json()
        except BaseException as e:
            print('[login] error is %s' % e)
        else:
            if res_json['code'] == '1':
                self._get_captcha(domain)

    def run(self):
        """
        入口
        :return:
        """
        self._login()


if __name__ == '__main__':
    scheduler = sched.scheduler(time, sleep)
    instance = AutoLogin()
    while True:
        scheduler.enter(86500, 0, instance.run(), ())
        scheduler.run()
