# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WangyiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class TrueloveItem(scrapy.Item):
    Nickname = scrapy.Field()
    Nameid = scrapy.Field()
    Age = scrapy.Field()
    Marital_status = scrapy.Field()
    Vocation = scrapy.Field()
    Height = scrapy.Field()
    Education = scrapy.Field()
    Constellation = scrapy.Field()
    Salay = scrapy.Field()
    Location = scrapy.Field()
    Origin = scrapy.Field()
    Monologue = scrapy.Field()