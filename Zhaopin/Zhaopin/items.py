# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhaopinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class ZhilianItem(scrapy.Item):
    url = scrapy.Field()
    company = scrapy.Field()
    position = scrapy.Field()
    salary = scrapy.Field()
    location = scrapy.Field()
    work_years = scrapy.Field()
    degree = scrapy.Field()
    position_type = scrapy.Field()
    tags=scrapy.Field()
    pub_data = scrapy.Field()
    position_desc = scrapy.Field()
    work_address = scrapy.Field()
