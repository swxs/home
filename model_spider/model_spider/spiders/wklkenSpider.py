# -*- coding: utf-8 -*-
# @Author  : SWXS
# @File    : wklkenSpider.py
# @Time    : 2018/1/31 23:51

import datetime
import scrapy
from scrapy import Request
from scrapy import Selector
from model_spider.model_spider.items import ArticalItem
from api.artical.creater import Creater as artical_creater


class WklkenSpider(scrapy.Spider):
    # spider名字
    name = "wklken"

    # 初始urls
    start_urls = [
        "http://www.wklken.me/",
    ]

    custom_settings = {
        # item处理管道
        'ITEM_PIPELINES': {},
    }

    def get_url(self, selector):
        return selector.css('a.title::attr(href)').extract_first()

    def is_yestaerday_artical(self, time):
        return (datetime.datetime.combine(datetime.date.today(), datetime.time.min) - datetime.timedelta(days=1)) == \
               datetime.datetime.strptime(time, "%Y/%m/%d")

    # 默认response处理函数
    def parse(self, response):
        sel = Selector(text=response.body)
        next_page_list = sel.css('p.paginator>a::attr(href)').extract()
        for next_page in next_page_list:
            yield Request(next_page,
                          method="GET",
                          callback=self.parse)

        artical_html_list = sel.css('li.article')
        for artical_html in artical_html_list:
            artical_sel = Selector(text=artical_html.extract())
            artical_item = ArticalItem()
            if self.get_url(artical_sel) is not None:
                yield Request(self.get_url(artical_sel),
                              method="GET",
                              meta=artical_item,
                              callback=self.content_parse)

    def content_parse(self, response):
        artical_sel = Selector(text=response.body)
        artical_item = ArticalItem()
        artical_item["title"] = artical_sel.css('article#article>section#header>h1::text').extract_first()
        artical_item["summary"] = artical_sel.css('article#article>section#header>h1::text').extract_first()
        artical_item["author"] = "wklken"
        artical_item["source"] = response.url
        artical_item["content"] = artical_sel.css('article#article>section#content').extract_first()

        artical_creater.create_artical(**dict(author=artical_item["author"],
                                              title=artical_item["title"],
                                              source=artical_item["source"],
                                              summary=artical_item["summary"],
                                              content=artical_item["content"]))
