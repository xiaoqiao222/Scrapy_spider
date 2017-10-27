# -*- coding: utf-8 -*-
import scrapy
import hashlib
from lxml import etree
from Zhaopin.items import ZhilianItem
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import CrawlSpider,Rule
from scrapy_redis.spiders import RedisCrawlSpider
import re

class ZhilianSpider(RedisCrawlSpider):
    name = 'zhilian'
    allowed_domains = ['zhaopin.com']

    redis_key = 'zhilian:start_urls'
    start_urls = ['http://sou.zhaopin.com']
    rules =  {
        Rule(LinkExtractor(allow=r'http://sou.zhaopin.com/jobs/'),follow=True),
        Rule(LinkExtractor(allow=r'jobs'), callback='parse_detail', follow=True),
    }
    def parse_detail(self,response):
        item =ZhilianItem()
        #html = response.body
        #用匿名函数进行判断
        f = lambda x: x if x else ''
        #公司名称
        company=f(response.xpath('//div[@class="tab-cont-box"]//h5/a[1]/text()').extract()[0])
        print company
        #职位名称
        position=f(response.xpath('//div[@class="top-fixed-box"]//h1/text()').extract()[0])
        print position
         #工资
        salary = f(response.xpath('//ul[@class="terminal-ul clearfix"]/li[1]/strong/text()').extract()[0])
        #转成字符
        print type(salary)
        location=f(response.xpath('//ul[@class="terminal-ul clearfix"]/li[2]//a/text()').extract()[0])
        print location
         #工作经验
        work_years=f(response.xpath('//ul[@class="terminal-ul clearfix"]/li[5]/strong/text()').extract()[0])
        print work_years
         #学历
        degree =f(response.xpath('//ul[@class="terminal-ul clearfix"]/li[6]/strong/text()').extract()[0])
        print degree
         #职位类型
        position_type= f(response.xpath('//ul[@class="terminal-ul clearfix"]/li[8]//a/text()').extract()[0])
        print position_type
         #标签
        tags=f(response.xpath('//div[@class="welfare-tab-box"]/span/text()').extract())
        print ''.join(tags)
         #发布日期
        pub_data=f(response.xpath('//ul[@class="terminal-ul clearfix"]/li[3]/strong/span/text()').extract()[0])
        print pub_data
         #职位简介
        position_desc=f(response.xpath('//div[@class="tab-cont-box"]//p/text()').extract())
        print position_desc
        #工作地址
        work_address=f(response.xpath('//div[@class="company-box"]//ul[@class="terminal-ul clearfix terminal-company mt20"]/li[4]/strong/text()').extract())
        print work_address
        item['url'] = self.md5(response.url)
        item['company']=company
        item['position']=position
        item['salary']=salary
        item['location']=location
        item['work_years']=work_years
        item['degree']=degree
        item['position_type']=position_type
        item['tags']=tags
        item['pub_data']=pub_data
        item['position_desc']=position_desc
        item['work_address']=work_address
        yield item
    def md5(self,data):
        m = hashlib.md5()
        m.update(data)
        return m.hexdigest()









