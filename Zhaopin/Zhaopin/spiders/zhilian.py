# -*- coding: utf-8 -*-
import scrapy
import hashlib
from lxml import etree
from Zhaopin.items import ZhilianItem
from scrapy_redis.spiders import RedisSpider
import re

class ZhilianSpider(RedisSpider):
    name = 'zhilian'
    allowed_domains = ['zhaopin.com']
    #start_urls = ['http://sou.zhaopin.com/assets/javascript/basedata.js?v=20170823']
    redis_key = 'zhilian:start_urls'
    headers ={
        "Host" : "sou.zhaopin.com" ,
        "Connection" : "keep-alive" ,
        "Cache-Control" : "max-age=0" ,
        "Upgrade-Insecure-Requests" : "1" ,
        "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36" ,
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8" ,
        "Referer" : "http://www.zhaopin.com/" ,
       # "Accept-Encoding" : "gzip, deflate" ,
        "Accept-Language" : "zh-CN,zh;q=0.8" ,
    }
    headers_x = {
        'Host': 'jobs.zhaopin.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
       # 'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
    }
    cookies ={
        "LastCity" : "%e5%8c%97%e4%ba%ac",
        "LastCity%5Fid" : "530",
        "dywez=95841923.1508721977.3.3.dywecsr=zhaopin.com|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct" : "/",
        "_jzqckmp" : "1",
        "firstchannelurl" : "https%3A//passport.zhaopin.com/findpassword/email/step1%3Fy7bRbP%3DdrDrq7vxnQvxnQvxQjyESn6j78vVCSUjRRLM0nBEU79",
        "lastchannelurl" : "https%3A//passport.zhaopin.com/findpassword/mobile/step3",
        "monitorlogin" : "Y",
        "dywem" : "95841923.y",
        "loginreleased" : "1",
        "pcc=r=190637629&t" : "1",
        "_jzqx=1.1508122808.1508725163.1.jzqsr=zhaopin%2Ecom|jzqct" : "/.-",
        "__xsptplus30" : "30.4.1508725162.1508725162.1%234%7C%7C%7C%7C%7C%23%23ZofmvZ_nqjDIrbr5Bv64Sp4qjp5rmwy4%23",
        "JsNewlogin" : "2083379858",
        "JSloginnamecookie" : "13994853013",
        "at" : "104d077725584918ae2e5fc8d52f2444",
        "Token" : "104d077725584918ae2e5fc8d52f2444",
        "rt" : "d0a05ac4607343fc80fa399bb0941e4e",
        "JSpUserInfo" : "3D753D6857645E7540685E645C754C68536451754C685864537535682464557548685964517540685E6450754C68596458754868596453753C682764557548685B6450754C6858645F754A6853645B754E682A641975086844640B751668076453752A683E6455754868516429752D6857645975496847645A754A684A64597549685064597540685164297535685764597542683F64297544682064257540685E645C754C68536451754C6858645A7542683F643C7544685B6453752A68236455754C685A64587548685A645875486851643D7529682464557548685964517540685E6450754C68596458754868596453753",
        "uiioit" : "2179306559640E375D77006451744C745C645D38026445345F6536793065596408375F773",
        "JSweixinNum" : "3",
        "JSSearchModel" : "0",
        "urlfrom" : "121126445",
        "urlfrom2" : "121126445",
        "adfcid" : "none",
        "adfcid2" : "none",
        "adfbid" : "0",
        "adfbid2" : "0",
        "usermob" : "536254724075536A56625F724C75596A526256724A756",
        "userphoto" : "",
        "userwork" : "0",
        "bindmob" : "2",
        "JSShowname" : "%e4%b9%94%e5%ae%bd%e5%ae%bd",
        "rinfo" : "JM944599522R90250000000_1",
        "Hm_lvt_38ba284938d5eddca645bb5e02a02006" : "1508122806,1508236171,1508721977",
        "Hm_lpvt_38ba284938d5eddca645bb5e02a02006" : "1508728400",
        "__utmt" : "1",
        "LastJobTag" : "%e4%ba%94%e9%99%a9%e4%b8%80%e9%87%91%7c%e7%bb%a9%e6%95%88%e5%a5%96%e9%87%91%7c%e8%8a%82%e6%97%a5%e7%a6%8f%e5%88%a9%7c%e5%91%98%e5%b7%a5%e6%97%85%e6%b8%b8%7c%e5%b8%a6%e8%96%aa%e5%b9%b4%e5%81%87%7c%e5%bc%b9%e6%80%a7%e5%b7%a5%e4%bd%9c%7c%e5%85%a8%e5%8b%a4%e5%a5%96%7c%e5%ae%9a%e6%9c%9f%e4%bd%93%e6%a3%80%7c%e8%a1%a5%e5%85%85%e5%8c%bb%e7%96%97%e4%bf%9d%e9%99%a9%7c%e9%a4%90%e8%a1%a5%7c%e4%ba%a4%e9%80%9a%e8%a1%a5%e5%8a%a9%7c%e5%b9%b4%e5%ba%95%e5%8f%8c%e8%96%aa%7c%e9%80%9a%e8%ae%af%e8%a1%a5%e8%b4%b4%7c%e5%b9%b4%e7%bb%88%e5%88%86%e7%ba%a2%7c%e5%8c%85%e4%bd%8f%7c%e5%8a%a0%e7%8f%ad%e8%a1%a5%e5%8a%a9%7c%e9%ab%98%e6%b8%a9%e8%a1%a5%e8%b4%b4%7c%e6%88%bf%e8%a1%a5%7c%e5%85%8d%e8%b4%b9%e7%8f%ad%e8%bd%a6%7c%e8%82%a1%e7%a5%a8%e6%9c%9f%e6%9d%83%7c%e5%8c%85%e5%90%83%7c%e4%b8%8d%e5%8a%a0%e7%8f%ad%7c%e6%af%8f%e5%b9%b4%e5%a4%9a%e6%ac%a1%e8%b0%83%e8%96%aa%7c%e5%88%9b%e4%b8%9a%e5%85%ac%e5%8f%b8%7c%e9%87%87%e6%9a%96%e8%a1%a5%e8%b4%b4%7c%e6%97%a0%e8%af%95%e7%94%a8%e6%9c%9f%7c%e4%bd%8f%e6%88%bf%e8%a1%a5%e8%b4%b4%7c14%e8%96%aa%7c%e5%81%a5%e8%ba%ab%e4%bf%b1%e4%b9%90%e9%83%a8%7c%e5%85%8d%e6%81%af%e6%88%bf%e8%b4%b7",
        "LastSearchHistory" : "%7b%22Id%22%3a%2274006b90-fa11-4700-b354-b30fb094c065%22%2c%22Name%22%3a%22%e5%8c%97%e4%ba%ac+%2b+%e9%94%80%e5%94%ae%e4%b8%9a%e5%8a%a1+%2b+%e9%94%80%e5%94%ae%e4%bb%a3%e8%a1%a8%22%2c%22SearchUrl%22%3a%22http%3a%2f%2fsou.zhaopin.com%2fjobs%2fsearchresult.ashx%3fjl%3d530%26bj%3d4010200%26sj%3d006%22%2c%22SaveTime%22%3a%22%5c%2fDate(1508728655348%2b0800)%5c%2f%22%7d",
        "_qzja" : "1.1756564954.1508122846682.1508723287430.1508725233533.1508728640825.1508728655546.0.0.0.73.4",
        "_qzjb" : "1.1508725233533.60.0.0.0",
        "_qzjc" : "1",
        "_qzjto" : "62.2.0",
        "_jzqa" : "1.734137436713493500.1508122808.1508721978.1508725163.4",
        "_jzqc" : "1",
        "_jzqb" : "1.63.10.1508725163.1",
        "dywea" : "95841923.754292184920911500.1508122802.1508236167.1508721977.3",
        "dywec" : "95841923",
        "dyweb" : "95841923.153.9.1508728679895",
        "__utma" : "269921210.1178085266.1508122802.1508236170.1508721978.3",
        "__utmb" : "269921210.154.9.1508728679903",
        "__utmc" : "269921210",
        "__utmz=269921210.1508721978.3.3.utmcsr=zhaopin.com|utmccn=(referral)|utmcmd=referral|utmcct" : "/",

    }
    def parse(self,response):
        print  1111
        start_url = 'http://sou.zhaopin.com/assets/javascript/basedata.js?v=20170823'
        yield scrapy.Request(url=start_url,callback=self.parse_cont,headers=self.headers,cookies=self.cookies,dont_filter=False)
    def parse_cont(self,response):
        print 222
        html= response.body.decode('utf-8')
        print html
        '''
        提取行业类别
        #第一次匹配
        dIndustryfrist =re.compile(r'dIndustry=.*')
        dIndustryall=dIndustryfrist.findall(html)
        #转成string
        dIndustryalls = '|'.join(dIndustryall)
        #第二次匹配
        dIndustrtwo = re.compile(r'\d+\@\d+|\@\d+|\d+\@')
        dIndustr =dIndustrtwo.findall(dIndustryalls)
        # ------------------------------------------------
        '''
        '''提取城市'''
        #第一次匹配
        # dCityfrist =re.compile(r"dCity =.*")
        # dCityall=dCityfrist.findall(html)
        #  # 转成string
        # dCityalls = '|'.join(dCityall)
        # #第二次匹配
        # dCitytwo = re.compile(ur'[\u4e00-\u9fa5]+')
        # dCity_list =dCitytwo.findall(dCityalls)
        # del dCity_list[0]
        # 第一次 获取 var dCity 后面的城市信息 ID+城市
        pattern = re.compile(r"var dCity = '(.*?)0@';")
        city_info = pattern.findall(html)
        print city_info
        city_info2 = city_info[0]
        # 第二次获取中文字段的城市(unicode格式)
        chn = re.compile(ur'[\u4e00-\u9fa5]+')
        city_list = chn.findall(city_info2)
        citys = []
        for city in city_list:
            city = city.encode("utf-8")
            citys.append(city)
        # 排除掉的省
        sheng= ['全国','广东','湖北','陕西','四川','辽宁','吉林','江苏','山东','浙江','广西','安徽','河北','山西','内蒙','黑龙江','福建','江西','河南','湖南','海南','贵州','云南','西藏','甘肃','青海','宁夏','新疆']
        s = set(sheng)
        citys = set(citys)
        # 存 放城市 ,对称差集更新操作
        citys.symmetric_difference_update(s)
        # 最终获取筛选出来的城市
        city_list = list(citys)
        print city_list
        '''
        #提取职业类别
        dJobtypefrist =re.compile(r"dJobtype=.*")
        dJobtypeall=dJobtypefrist.findall(html)
         # 转成string
        dJobtypealls = '|'.join(dJobtypeall)
        #第二次匹配
        print dJobtypealls
        dJobtypetwo = re.compile(r'\d+\@\d+|\@\d+|\d+\@')
        dJobtype =dJobtypetwo.findall(dJobtypealls)

        print dJobtype
        print type(dJobtype)
        '''
        '''学历信息  从接口匹配
        dDegreefrist =re.compile(r"dDegree=.*")
        dDegreeall=dDegreefrist.findall(html)
         # 转成string
        dDegreealls = '|'.join(dDegreeall)
        #第二次匹配
        dDegreetwo = re.compile(r'\d|\-\d')
        dDegree_list =dDegreetwo.findall(dDegreealls)
        ---------------------
        '''
        # 学历 自己创建
        dDegree_list = [-1,1,3,4,5,7,8]
        print dDegree_list
        '''企业性质 借口匹配
        dComptypefrist =re.compile(r"dComptype =.*")
        dComptypeall=dComptypefrist.findall(html)
         # 转成string
        dComptypealls = '|'.join(dComptypeall)
        #第二次匹配
        # print dComptypealls
        dComptypetwo = re.compile(r'\@(\d{1,2})')
        dComptype_list =dComptypetwo.findall(dComptypealls)
        '''
        # 公司性质
        dComptype_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
        print dComptype_list
        # 职位类型
        Positiontype_list = [1,2,4,5]
        base_url='http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%s&ct=%s&et=%s&el=%s'
        for jl in city_list:
            print jl
            print type(jl)
            for ct in dDegree_list:
                for et in Positiontype_list:
                    for el in dComptype_list:
                        full_url=base_url %(str(jl),str(ct),str(et),str(el))
                        #print full_url
                        yield scrapy.Request(full_url,callback=self.parse_list,headers=self.headers,cookies=self.cookies)
        # base_url='http://sou.zhaopin.com/jobs/searchresult.ashx?jl=北京&ct=-1&el=1&p=%s'
        # for p in range(1,91):
        #     full_url=base_url %str(p)
        #     yield scrapy.Request(full_url,callback=self.parse,headers=self.headers,cookies=self.cookies)
    def parse_list(self, response):
        for i in response.xpath('//div[@id="newlist_list_content_table"]//div/a/@href').extract():
            if 'jobs.zhaopin.com' in i:
                print i
                yield scrapy.Request(url=i,callback=self.parse_details,headers=self.headers_x,cookies=self.cookies,priority=1)
        next_page = response.xpath('//a[@class="next-page"]/@href').extract()
        if next_page:
            yield scrapy.Request(next_page[0],callback=self.parse_list)
    def parse_details(self,response):
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









