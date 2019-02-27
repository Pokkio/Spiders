# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import YunqiBookListItem, YunqiBookDetailItem
from scrapy_redis.spiders import RedisSpider


class YunqiQqComSpider(RedisSpider, CrawlSpider):
    name = 'yunqi.qq.com'
    allowed_domains = ['yunqi.qq.com']
    start_urls = ['http://yunqi.qq.com/bk/so2/n30p1']

    rules = (
        Rule(LinkExtractor(allow=r'/bk/so2/n30p\d+'), callback='parse_book_list', follow=True),
    )

    def parse_book_list(self, response):
        books = response.xpath(".//div[@class='book']")
        for book in books:
            novel_image_url = book.xpath("./a/img/@src").extract_first()
            novel_id = book.xpath("./div[@class='book_info']/h3/a/@id").extract_first()
            novel_name = book.xpath("./div[@class='book_info']/h3/a/text()").extract_first()
            novel_link = book.xpath("./div[@class='book_info']/h3/a/@href").extract_first()
            novel_infos = book.xpath("./div[@class='book_info']/dl/dd[@class='w_auth']")
            if len(novel_infos) > 4:
                novel_author = novel_infos[0].xpath('./a/text()').extract_first()
                novel_type = novel_infos[1].xpath('./a/text()').extract_first()
                novel_status = novel_infos[2].xpath('./text()').extract_first()
                novel_update_time = novel_infos[3].xpath('./text()').extract_first()
                novel_words = novel_infos[4].xpath('./text()').extract_first()
            else:
                novel_author = ''
                novel_type = ''
                novel_status = ''
                novel_update_time = ''
                novel_words = 0
            print(novel_link)
            book_list_item = YunqiBookListItem(novelId=novel_id, novelName=novel_name,
                                               novelLink=novel_link, novelAuthor=novel_author,
                                               novelType=novel_type, novelStatus=novel_status,
                                               novelUpdateTime=novel_update_time, novelWords=novel_words,
                                               novelImageUrl=novel_image_url)
            yield book_list_item

            request = scrapy.Request(url=novel_link, callback=self.parse_book_detail)
            request.meta['novel_id'] = novel_id
            yield request

    def parse_book_detail(self, response):
        novel_id = response.meta['novel_id']
        novel_label = response.xpath("//div[@class='tags']/text()").extract_first()
        novel_all_click = response.xpath(".//*[@id='novelInfo']/table/tr[2]/td[1]/text()").extract_first()
        novel_all_popular = response.xpath(".//*[@id='novelInfo']/table/tr[2]/td[2]/text()").extract_first()
        novel_all_comm = response.xpath(".//*[@id='novelInfo']/table/tr[2]/td[3]/text()").extract_first()
        novel_month_click = response.xpath(".//*[@id='novelInfo']/table/tr[3]/td[1]/text()").extract_first()
        novel_month_popular = response.xpath(".//*[@id='novelInfo']/table/tr[3]/td[2]/text()").extract_first()
        novel_month_comm = response.xpath(".//*[@id='novelInfo']/table/tr[3]/td[3]/text()").extract_first()
        novel_week_click = response.xpath(".//*[@id='novelInfo']/table/tr[4]/td[1]/text()").extract_first()
        novel_week_popular = response.xpath(".//*[@id='novelInfo']/table/tr[4]/td[2]/text()").extract_first()
        novel_week_comm = response.xpath(".//*[@id='novelInfo']/table/tr[4]/td[3]/text()").extract_first()
        novel_comment_num = response.xpath(".//*[@id='novelInfo_commentCount']/text()").extract_first()
        book_detail_item = YunqiBookDetailItem(novelId=novel_id, novelLabel=novel_label,
                                               novelAllClick=novel_all_click, novelAllPopular=novel_all_popular,
                                               novelAllComm=novel_all_comm, novelMonthClick=novel_month_click,
                                               novelMonthPopular=novel_month_popular, novelMonthComm=novel_month_comm,
                                               novelWeekClick=novel_week_click, novelWeekPopular=novel_week_popular,
                                               novelWeekComm=novel_week_comm, novelCommentNum=novel_comment_num)
        yield book_detail_item
