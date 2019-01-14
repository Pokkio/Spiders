import requests
from lxml import etree
from fontTools.ttLib import TTFont
import re
from autohome.proxies import Proxy


class Autohome:
    def __init__(self):
        pass

    @staticmethod
    def get_html():
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/59.0.3071.86 Safari/537.36',
            'host': 'club.autohome.com.cn'
        }
        ttf_name = 'font/auto.ttf'
        url = 'https://club.autohome.com.cn/bbs/thread/bf9817b6ec7ad790/78316566-1.html#pvareaid=6825493'
        resp_code = requests.get(url, headers)  # 获取页面源码
        ttf_pattern = re.compile(r",url\('(//.*.ttf)'\)")
        ttf_re = re.search(ttf_pattern, resp_code.text)  # 获取ttf字体部分链接
        try:
            if ttf_re:
                ttf_url = 'https:' + ttf_re.group(1)  # ttf 完整链接
                ttf_file_stream = requests.get(ttf_url, headers, stream=True)  # 以文件流形式返回
                with open(ttf_name, 'wb') as f:
                    for chunk in ttf_file_stream.iter_content(chunk_size=1024):
                        f.write(chunk)
                ttf = TTFont(ttf_name)  # 解析字体库文件
                word_unicode_list = ttf['cmap'].tables[0].ttFont.getGlyphOrder()  # 各个字符的unicode编码
                '''
                >>> word_unicode_List
                ['.notdef', 'uniED8F', 'uniED3D', …… ]
                '''
                print('自定义字体列表unicode编码: {}'.format(word_unicode_list[1:]))
                word_utf8_list = [eval("u'\\u" + uniword[3:] + "'").encode('utf8') for uniword in
                                  word_unicode_list[1:]]  # unicode->utf8
                '''
                >>> word_utf8_list
                [b'\xee\xb6\x8f', b'\xee\xb4\xbd', b'\xee\xb7\xb1']
                '''
                print('自定义字体列表utf8编码: {}'.format(word_utf8_list))
                resp_text = etree.HTML(resp_code.text)
                content_list = resp_text.xpath("//div[@class='tz-paragraph']/text()")  # 获取段落文本

                content = ''.encode('utf8')
                for elem in content_list:  # 以 utf8 编码保存文本的原内容
                    content += elem.encode('utf8')

                word_list = ['是', '呢', '二', '九', '了', '近', '和', '更', '短',
                             '左', '低', '十', '高', '下', '右', '少', '很', '矮',
                             '的', '好', '地', '着', '三', '上', '八', '不', '长',
                             '得', '远', '多', '坏', '六', '四', '大', '小', '七',
                             '五', '一']  # unicode编码
                print('字体文件中字形列表: {}'.format(word_list))
                print('content_before: {}'.format(content.decode('utf8')))
                print('------------------After Convert------------------')
                for index in range(len(word_utf8_list)):
                    content = content.replace(word_utf8_list[index], word_list[index].encode('utf8'))
                print('content_after: {}'.format(content.decode('utf8')))
            else:
                print('匹配字体链接失败，请添加ip代理！')
        except AssertionError:
            print('获取ttf字体文件资源失败！')
        except (BaseException, TimeoutError) as e:
            print('爬取错误: %s' % e)


if __name__ == '__main__':
    Autohome().get_html()
