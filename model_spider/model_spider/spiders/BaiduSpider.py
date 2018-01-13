# -*- coding: utf-8 -*-"
import datetime
import scrapy
from scrapy import Request
from scrapy import Selector


class BaiduSpider(scrapy.Spider):
    # spider名字
    name = "jobbole"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36",
    }

    @classmethod
    def getCookies(cls):
        cookies = "BDRCVFR[mkUqnUt8juD]=mk3SLVN4HKm; bd_traffictrace=262211_262211; plus_lsv=c8b9e76f0143a502; plus_cv=1::m:21732389; Hm_lvt_12423ecbc0e2ca965d84259063d35238=1503756700; Hm_lpvt_12423ecbc0e2ca965d84259063d35238=1503756710; BDUSS=lhZZFFyUkNqWGVWdXR4SWpUa09YakF6OWx-dzI0UVZXVUV5YzB0azFBaUVHTWxaTVFBQUFBJCQAAAAAAAAAAAEAAADO5JYRaWFtb29tAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAISLoVmEi6FZd; H_WISE_SIDS=118417_110315_114550_117615_113879_104886_100097_118505_106200_118943_118870_118833_118794_118696_118272_118156_118674_107319_118450_118145_118234_117274_117587_117238_117432_118122_118326_118324_118133_118218_115536_118102_117550_118141_117635_118322_115137_114820_116408_110085; BAIDU_WISE_UID=wapp_1503760380685_793; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; BD_CK_SAM=1; PSINO=5; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BD_HOME=1; H_PS_PSSID=1455_21091_17001_20929; BD_UPN=12314753; sug=0; sugstore=1; ORIGIN=0; bdime=0"
        cookie = dict()
        for ck in cookies.split(";"):
            name, value = ck.strip().split('=', 1)
            cookie[name] = value
        return cookie

    # 初始urls
    start_urls = [
        "http://tieba.baidu.com/mo/",
    ]

    custom_settings = {
        # item处理管道
        'ITEM_PIPELINES': {},
    }

    def start_requests(self):
        ''' 覆盖默认的方法(忽略start_urls)'''
        yield Request('http://tieba.baidu.com/mo/',
                      method="GET",
                      headers=BaiduSpider.headers,
                      cookies=BaiduSpider.getCookies(),
                      callback=self.get_url_parser)
        # 默认response处理函数

    def parse(self, response):
        sel = Selector(text=response.body)
        pass

    def get_url_parser(self, response):
        sel = Selector(text=response.body)
        for i in range(10):
            yield Request('http://www.example.com/list/1?page={0}'.format(i))
        pass
