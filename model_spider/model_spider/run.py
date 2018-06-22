# -*- coding: utf-8 -*-"

import sys
import os
if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.curdir))

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from .spiders.JobboleSpider import JobboleSpider
from .spiders.BaiduSpider import BaiduSpider
from .spiders.wklkenSpider import WklkenSpider
from .spiders.BossZhipinSpider import BossZhipinSpider

def run():
    # 获取settings.py模块的设置
    settings = get_project_settings()
    process = CrawlerProcess(settings=settings)

    # 可以添加多个spider
    # process.crawl(JobboleSpider)
    # process.crawl(BaiduSpider)
    # process.crawl(WklkenSpider)  # not daily
    process.crawl(BossZhipinSpider) # not daily

    # 启动爬虫，会阻塞，直到爬取完成
    process.start()

if __name__ == "__main__":
    run()