# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class WangyiPipeline(object):
    def process_item(self, item, spider):
        return item
class TruelovePipeline(object):
    def __init__(self):
        self.f = open('truelove.json','w')
     # 必须要实现的方法就是,处理item
    def process_item(self,item,spider):
        self.f.write(json.dumps(dict(item),ensure_ascii=False).encode('utf-8') + '\n')
        print  1111
        return item

    def close_spider(self,spider):
        self.f.close()