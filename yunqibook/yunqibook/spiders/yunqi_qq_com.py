# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from ..items import YunqiBookListItem, YunqiBookDetailItem
from scrapy_redis.spiders import RedisCrawlSpider


class YunqiQqComSpider(RedisCrawlSpider):
    name = 'yunqi.qq.com'
    allowed_domains = ['yunqi.qq.com']
    # start_urls = ['http://yunqi.qq.com/bk/so2/n30p1']
    redis_key = 'yunqispider'

    # XXX(CLay): a ',' should be added at the end of the 'Rule', or an typeerror will be reported.
    rules = (
        Rule(LinkExtractor(allow=r'(.*)?/bk/zp200so2/n30p\d+'), callback='parse_book_list', follow=True),
    )

    def parse_book_list(self, response):
        try:
            res_xpath = etree.HTML(response.text)
            for book in res_xpath.xpath("//*[@id='detailedBookList']/div[@class='book']"):
                # TODO(CLay): perfecting functions about extraction errors.
                novel_id = book.xpath(".//div[@class='book_info']/h3/a/@id")[0]
                novel_name = book.xpath(".//div[@class='book_info']/h3/a/text()")[0]
                novel_link = book.xpath(".//div[@class='book_info']/h3/a/@href")[0]
                novel_info = book.xpath(".//div[@class='book_info']/dl/dd[@class='book_intro']")[0].text.replace('\n', '').replace('\r\n', '').replace('...', '').replace('\r', '')
                novel_author = book.xpath(".//dl/dd[@class='w_auth']")[0].xpath('a')[0].text
                novel_type = book.xpath(".//dl/dd[@class='w_auth']")[1].xpath('a')[0].text.replace('[', '').replace(']', '')
                novel_status = book.xpath(".//dl/dd[@class='w_auth']")[2].text
                novel_update_time = '20' + book.xpath(".//dl[2]/dd[@class='w_auth']")[0].text
                novel_words = book.xpath(".//dl[2]/dd[@class='w_auth']")[1].text
                book_list_item = YunqiBookListItem(novelId=novel_id, novelName=novel_name,
                                                   novelLink=novel_link, novelAuthor=novel_author,
                                                   novelType=novel_type, novelStatus=novel_status,
                                                   novelUpdateTime=novel_update_time,
                                                   novelWords=novel_words, novelInfo=novel_info)
                yield book_list_item

                request = scrapy.Request(url=novel_link, callback=self.parse_book_detail)
                request.meta['data'] = {'novelId': novel_id if novel_id else None, 'novelName': novel_name
                                        if novel_name else None}
                yield request
        except (BaseException, TimeoutError, ConnectionError, AttributeError, IndexError) as e:
            print('falied: %s' % e)

    def parse_book_detail(self, response):
        try:
            data = response.meta['data']
            res_xpath = etree.HTML(response.text)
            novel_label = res_xpath.xpath("//*[@class='tags']")[0].text.replace('作品标签', '').replace('  ', '').replace('：', '').replace('\n', '')
            tr2_xpath = res_xpath.xpath('//div[@id="novelInfo"]/table/tr[2]')[0]
            novel_all_click = tr2_xpath.xpath('td[1]')[0].text[5:]  # 总阅文点击
            novel_all_popular = tr2_xpath.xpath('td[2]')[0].text[4:]  # 总人气
            novel_all_comm = tr2_xpath.xpath('td[3]')[0].text[4:]  # 总推荐

            tr3_xpath = res_xpath.xpath('//div[@id="novelInfo"]/table/tr[3]')[0]
            novel_month_click = tr3_xpath.xpath('td[1]')[0].text[8:]  # 月阅文点击
            novel_month_popular = tr3_xpath.xpath('td[2]')[0].text[4:]  # 月人气
            novel_month_comm = tr3_xpath.xpath('td[3]')[0].text[4:]  # 月推荐

            tr4_xpath = res_xpath.xpath('//div[@id="novelInfo"]/table/tr[4]')[0]
            novel_week_click = tr4_xpath.xpath('td[1]')[0].text[8:]  # 周阅文点击
            novel_week_popular = tr4_xpath.xpath('td[2]')[0].text[4:]  # 周人气
            novel_week_comm = tr4_xpath.xpath('td[3]')[0].text[4:]  # 周推荐

            tr5_xpath = res_xpath.xpath('//div[@id="novelInfo"]/table/tr[5]')[0]
            novel_comment_num = tr5_xpath.xpath("td[2]")[0].text[4:]  # 评论数
            book_detail_item = YunqiBookDetailItem(novelId=data.get('novelId'),
                                                   novelLabel=novel_label, novelName=data.get('novelName'),
                                                   novelAllClick=novel_all_click, novelAllPopular=novel_all_popular,
                                                   novelAllComm=novel_all_comm, novelMonthClick=novel_month_click,
                                                   novelMonthPopular=novel_month_popular, novelMonthComm=novel_month_comm,
                                                   novelWeekClick=novel_week_click, novelWeekPopular=novel_week_popular,
                                                   novelWeekComm=novel_week_comm, novelCommentNum=novel_comment_num)
            yield book_detail_item
        except IndexError as e:
            print('falied: %s' % e)
