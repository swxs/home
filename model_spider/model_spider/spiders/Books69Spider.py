# -*- coding: utf-8 -*-
# @File    : Books69Spider.py
# @AUTH    : swxs
# @Time    : 2018/8/12 21:57

import datetime
import scrapy
from scrapy import Request
from scrapy import Selector


class Books69Spider(scrapy.Spider):
    # spider名字
    name = "book69"

    # 初始urls
    start_urls = [
        "http://www.69shu.org/book/81073/24645057.html",
    ]

    custom_settings = {}

    # 默认response处理函数
    def parse(self, response):
        sel = Selector(text=response.body.decode('gb18030').encode('utf8'))
        text_list = sel.css('div#htmlContent::text')
        with open("text2.txt", "a", encoding="utf8") as f:
            for text in text_list:
                f.write(text.extract())

        next_page_list = sel.css('a.pager_next::attr(href)').extract()
        for next_page in next_page_list:
            yield Request(next_page,
                          method="GET",
                          callback=self.parse)



