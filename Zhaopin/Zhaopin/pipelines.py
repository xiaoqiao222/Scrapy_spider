# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class ZhaopinPipeline(object):
    def process_item(self, item, spider):
        return item
# class ZhilianPipeline(object):
#     def __init__(self):
#         self.f = open('zhilian.json' ,'w')
#     # 必须要实现的方法就是,处理item
#     def process_item(self ,item, spider):
#         self.f.write(json.dumps(dict(item),ensure_ascii=False).encode('utf-8') + '\n')
#         return item
#
#     def close_spider(self,spider):
#         self.f.close()