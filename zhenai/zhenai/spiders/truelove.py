# -*- coding: utf-8 -*-
import scrapy
import  json
from lxml import etree
from zhenai.items import TrueloveItem
from scrapy_redis.spiders import RedisSpider
import re
class loveSpider(RedisSpider):

    name = 'truelove'
    allowed_domains = ['zhenai.com']
    redis_key = 'truelove:start_urls'
    headers = {
        "Host": "search.zhenai.com",
        "Connection": "keep-alive",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Referer": "http://search.zhenai.com/v2/search/pinterest.do?sex=1&agebegin=18&ageend=25&workcityprovince=-1&workcitycity=-1&h1=-1&h2=-1&salaryBegin=-1&salaryEnd=-1&occupation=-1&h=-1&c=-1&workcityprovince1=-1&workcitycity1=-1&constellation=-1&animals=-1&stock=-1&belief=-1&condition=66&orderby=hpf&hotIndex=&online=",
        # "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8",
    }
    cookies ={
        "CHANNEL=^~refererHost=bzclk.baidu.com^~channelId=900122^~subid" : "^~",
        "sid" : "KJKR7RGmvmGrYpovHcUl",
        "isSignOut" : "%5E%7ElastLoginActionTime%3D1508564808107%5E%7E",
        "p" : "%5E%7Eworkcity%3D10102008%5E%7Elh%3D108324720%5E%7Esex%3D0%5E%7Enickname%3D%E4%BC%9A%E5%91%98108324720%5E%7Emt%3D1%5E%7Eage%3D21%5E%7Edby%3D423975c5b070bcf3%5E%7E",
        "mid" : "%5E%7Emid%3D108324720%5E%7E",
        "loginactiontime" : "%5E%7Eloginactiontime%3D1508564808108%5E%7E",
        "logininfo" : "%5E%7Elogininfo%3D%5E%7E",
        "rmpwd" : "",
        "otherinfo" : "",
        "hds" : "2",
        "live800" : "%5E%7EisOfflineCity%3Dtrue%5E%7EinfoValue%3DuserId%253D108324720%2526name%253D108324720%2526memo%253D%5E%7E",
        "bottomRemind" : "%5E%7EvisPhoto%3Dno%5E%7E",
        "LOGIN_FIRST108324720" : "%5E%7EmemberId%3D108324720%5E%7EendDate%3D2017%E5%B9%B410%E6%9C%8825%E6%97%A5%5E%7Elogincount%3D1%5E%7E",
        "REG_LOGIN" : "%5E%7EnewUserFlag%3Dt%5E%7E",
        "__utma" : "185049014.722379128.1508564810.1508564810.1508564810.1",
        "__utmc" : "185049014",
        "__utmz=185049014.1508564810.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd" : "(none)",
        "JSESSIONID" : "abcNOi54zMlrS5jJpE98v",
        "Hm_lvt_2c8ad67df9e787ad29dbd54ee608f5d2" : "1508482992,1508564795",
        "Hm_lpvt_2c8ad67df9e787ad29dbd54ee608f5d2" : "1508568600",
        "__xsptplus14" : "14.2.1508567275.1508568599.5%234%7C%7C%7C%7C%7C%23%23ZqVAO0XWXFcNMgx4Hk8SK_3nekXipANV%23",

    }
    def parse(self,response):
        print 111
        start_url = 'http://search.zhenai.com/v2/search/pinterest.do'
        yield scrapy.Request(url=start_url,callback=self.parse_cont,headers=self.headers,cookies=self.cookies,dont_filter=True)
    def parse_cont(self,response):
        print 222
        sex_list = ['1']
        age_list = range(18,100)
        province = {}
        with open('city.html','r') as f:
            html = etree.HTML(f.read())
            city_div = html.xpath('//div[@class="city_box"]')
            for city in city_div:
                city_id_list = city.xpath('.//a/@v')
                property_id = city_id_list[0][:-2]+'00'
                province[str(property_id)] = city_id_list
        for key,value in province.items():
            print key,value
        base_url='http://search.zhenai.com/v2/search/getPinterestData.do?sex=%s&agebegin=%s&ageend=%s&workcityprovince=%s&workcitycity=%s&h1=-1&h2=-1&salaryBegin=-1&salaryEnd=-1&occupation=-1&h=-1&c=-1&workcityprovince1=-1&workcitycity1=-1&constellation=-1&animals=-1&stock=-1&belief=-1&condition=66&orderby=hpf&hotIndex=0&online=&currentpage=%s&topSearch=false'
        for sex in sex_list:
            for age in age_list:
                for proid,city_list in province.items():
                    for cityid in city_list:
                        for page in range(1,101):
                            full_url=base_url % (str(sex),str(age),str(age),str(proid),str(cityid),str(page))
                            yield scrapy.Request(full_url,callback=self.pares_list,headers=self.headers,cookies=self.cookies,)
       # base_url = 'http://search.zhenai.com/v2/search/getPinterestData.do?sex=%s&agebegin=-1&ageend=-1&workcityprovince=-1&workcitycity=-1&h1=-1&h2=-1&salaryBegin=-1&salaryEnd=-1&occupation=-1&h=-1&c=-1&workcityprovince1=-1&workcitycity1=-1&constellation=-1&animals=-1&stock=-1&belief=-1&condition=66&orderby=hpf&hotIndex=0&online=&currentpage=7&topSearch=false'
        # for sex in sex_list:
        #     # for page in range(1,101):
        #     full_url = base_url %(str(sex))
        #     yield scrapy.Request(full_url,callback=self.pares_detail,headers=self.headers,cookies=self.cookies)
    def pares_list(self,response):
        print 111111
        #print response.body.decode('gbk')
        html = response.body.decode('gbk')
        #print html
        paperid = re.compile(r'"memberId":(\d+)')
        paperid_list = paperid.findall(html)
        #print paperid_list
        for pipo in paperid_list:
            qingq_url='http://album.zhenai.com/u/'
            zong_url = qingq_url + pipo+'?flag=s'
            print(zong_url)
            yield scrapy.Request(url=zong_url,callback=self.parse_detail,headers=self.headers,cookies=self.cookies,priority=1)
    def parse_detail(self, response):
        item = TrueloveItem()
        f = lambda x: x if x else ''
        Nickname = response.xpath('//div[@class="brief-top p30"]/p/a/text()').extract()[0]
        print Nickname
        #ID
        Nameid = f(response.xpath('//p[@class="brief-info fs14 lh32 c9f"]/text()').extract()[0])
        #年龄
        Age = f(response.xpath('//table[@class="brief-table"]//td[1]/text()').extract()[0])
        # 婚况
        Marital_status = f(response.xpath('//table[@class="brief-table"]//td[1]/text()').extract()[1])
        # 职业
        Vocation = f(response.xpath('//table[@class="brief-table"]//td[1]/text()').extract()[2])
        #身高
        Height = f(response.xpath('//table[@class="brief-table"]//td[2]/text()').extract()[0])
        print Height
        #学历
        Education = f(response.xpath('//table[@class="brief-table"]//td[2]/text()').extract()[1])
        print Education
        #星座
        Constellation = f(response.xpath('//table[@class="brief-table"]//td[2]/text()').extract()[2])
        print Constellation
        #收入
        Salay = f(response.xpath('//table[@class="brief-table"]//td[3]/text()').extract()[0])
        print Salay
        #工作地
        Location = f(response.xpath('//table[@class="brief-table"]//td[3]/text()').extract()[1])
        #籍贯
        Origin = f(response.xpath('//table[@class="brief-table"]//td[3]/text()').extract()[2])
        print Origin
        #独白
        Monologue = f(response.xpath('//div[@class="info-text"]/p/text()').extract()[0])
        print Monologue
        item['Nickname'] = Nickname
        item['Nameid'] = Nameid
        item['Age'] = Age
        item['Marital_status'] = Marital_status
        item['Vocation'] = Vocation
        item['Height'] = Height
        item['Education'] = Education
        item['Constellation'] = Constellation
        item['Salay'] = Salay
        item['Location'] = Location
        item['Origin'] = Origin
        item['Monologue'] = Monologue
        yield item


