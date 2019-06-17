# -*- coding: utf-8 -*-
"""
    百度ocr文件
"""

from requests import get, post
import base64


class Ocr:
    """
    ocr类
    """

    # 百度ocr
    _API_KEY = 'xxxxx'
    _SECRET_KEY = 'xxxxx'
    _headers = {
        'Content-Type': 'application/json; charset=UTF-8'
    }
    _capt_headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    def _get_access_token(self):
        """
        获取 access_token
        :return:
        """
        url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={0}&client_secret={1}'.format(
            self._API_KEY, self._SECRET_KEY
        )
        res = get(url, self._headers, timeout=3).json()
        return res['access_token']

    def _download_captcha_and_encode(self, image_data):
        """
        验证图片
        :param image_data:
        :return:
        """
        access_token = self._get_access_token()
        url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=' + access_token
        form_data = {
            'image': base64.b64encode(image_data)
        }
        data = post(url, data=form_data, headers=self._capt_headers)
        res_code = data.json()['words_result'][0]['words'].replace(' ', '')
        return res_code

    def run(self, image_data):
        return self._download_captcha_and_encode(image_data)


if __name__ == '__main__':
    token = Ocr()