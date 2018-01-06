# -*- coding: utf-8 -*-"

from scrapy import Item, Field


class ArticalItem(Item):
    source = Field()
    title = Field()
    author = Field()
    summary = Field()
    content = Field()
