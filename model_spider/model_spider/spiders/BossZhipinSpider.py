# -*- coding: utf-8 -*-
# @File    : BossZhipinSpider.py
# @AUTH    : swxs
# @Time    : 2018/5/3 13:40

import datetime
import re
import scrapy
from scrapy import Request
from scrapy import Selector
from api.job import utils as job_utils
from const import undefined


class BossZhipinSpider(scrapy.Spider):
    # spider名字
    name = "boss_zhipin"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36",
    }

    # 初始urls
    start_urls = [
        "https://www.zhipin.com/c101020100/h_101020100/?query=大数据+算法&page=1&ka=page-1",
        "https://www.zhipin.com/c101020100/h_101020100/?query=大数据算法&page=1&ka=page-1",
        "https://www.zhipin.com/c101020100/h_101020100/?query=数据分析&page=1&ka=page-1",
        "https://www.zhipin.com/c101020100/h_101020100/?query=大数据&page=1&ka=page-1",
        # "https://www.zhipin.com/c101020100/b_%E5%98%89%E5%AE%9A%E5%8C%BA-h_101020100/?query=%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AE%97%E6%B3%95&page=1&ka=page-1",
    ]

    custom_settings = {
        # item处理管道
        'ITEM_PIPELINES': {},
    }

    def get_next_page_url(self, selector):
        if selector.css('a.next::attr(href)').extract_first():
            return "https://www.zhipin.com" + selector.css('a.next::attr(href)').extract_first()
        else:
            return False

    def get_url(self, selector):
        return selector.css('a.next::attr(href)').extract_first()

    # 默认response处理函数
    def parse(self, response):
        sel = Selector(text=response.body)
        job_html_list = sel.css('div.job-primary')
        for job_html in job_html_list:
            job_sel = Selector(text=job_html.extract())
            job_type = job_sel.css('div.job-title::text').extract_first()
            job_pay = job_sel.css('span.red::text').extract_first()
            job_city, job_age, job_edu = job_sel.css('p').extract()[0].replace('<p>', '').replace('</p>', '').split('<em class="vline"></em>')
            company_info = job_sel.css('p').extract()[1].replace('<p>', '').replace('</p>', '').split('<em class="vline"></em>')
            if len(company_info) == 2:
                job_company_type, job_company_pn = company_info
                job_company_kind = undefined
            else:
                job_company_type, job_company_kind, job_company_pn = company_info
            job_time = job_sel.css('p').extract()[2].replace('<p>', '').replace('</p>', '').split('<em class="vline"></em>')[0]
            job_company_name = job_sel.css('a::text').extract()[-1]
            job_url = u"https://www.zhipin.com" + job_sel.css('a::attr(href)').extract()[0]
            job = job_utils.get_job_by_type_company_name(job_type, job_company_name)
            if job is None:
                job_utils.create_job(
                    job_type=job_type,
                    job_pay=job_pay,
                    job_time=job_time,
                    job_city=job_city,
                    job_age=job_age,
                    job_edu=job_edu,
                    job_company_name=job_company_name,
                    job_company_type=job_company_type,
                    job_company_kind=job_company_kind,
                    job_company_pn=job_company_pn,
                    job_url=job_url
                )

        if self.get_next_page_url(sel):
            yield Request(self.get_next_page_url(sel),
                          method="GET",
                          callback=self.parse)
