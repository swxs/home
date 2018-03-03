# -*- coding: utf-8 -*-"
import datetime
import scrapy
from scrapy import Request
from scrapy import Selector
from model_spider.model_spider.items import ArticalItem
from api.artical import utils as artical_utils


class JobboleSpider(scrapy.Spider):
    # spider名字
    name = "jobbole"

    # 初始urls
    start_urls = [
        "http://web.jobbole.com/category/javascript-2/",
        "http://web.jobbole.com/category/css/",
        "http://python.jobbole.com/all-posts/",
    ]

    custom_settings = {
        # item处理管道
        'ITEM_PIPELINES': {},
    }

    def get_url(self, selector):
        return selector.css('a.archive-title::attr(href)').extract_first()

    def is_yestaerday_artical(self, time):
        return (datetime.datetime.combine(datetime.date.today(), datetime.time.min) - datetime.timedelta(days=1)) == \
               datetime.datetime.strptime(time, "%Y/%m/%d")

    # 默认response处理函数
    def parse(self, response):
        sel = Selector(text=response.body)
        artical_html_list = sel.css('div.post-meta')
        for artical_html in artical_html_list:
            artical_sel = Selector(text=artical_html.extract())
            artical_item = ArticalItem()
            artical_item["title"] = artical_sel.css('a.archive-title::attr(title)').extract_first()
            artical_item["summary"] = artical_sel.css('span.excerpt>p::text').extract_first()
            if self.get_url(artical_sel) is not None:
                yield Request(self.get_url(artical_sel),
                              method="GET",
                              meta=artical_item,
                              callback=self.content_parse)

    def content_parse(self, response):
        artical_sel = Selector(text=response.body)
        artical_item = ArticalItem()
        time_sel = Selector(text=artical_sel.css('.entry-meta > .entry-meta-hide-on-mobile::text').extract_first())
        time = time_sel.re(r"[0-9]{4}/[0-9]{2}/[0-9]{2}")[0]
        if self.is_yestaerday_artical(time):
            artical_item["title"] = response.meta.get('title')
            artical_item["summary"] = response.meta.get('summary')
            artical_item["author"] = artical_sel.css('div.copyright-area>a::text').extract_first()
            artical_item["source"] = artical_sel.css('div.copyright-area>a::attr(href)').extract_first()
            artical_item["content"] = artical_sel.css('div.entry').extract_first()

            artical_utils.create_artical(**dict(author=artical_item["author"],
                                                title=artical_item["title"],
                                                source=artical_item["source"],
                                                summary=artical_item["summary"],
                                                content=artical_item["content"]))
