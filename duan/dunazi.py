#coding utf8
from selenium import webdriver
from lxml import etree
import time
import requests
import json,re
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
)
browser = webdriver.PhantomJS()
print 1111
browser.get('http://neihanshequ.com/')
time.sleep(3)
browser.save_screenshot('daunzi.png')
time.sleep(1)
for i in range(6):
    print 3

    time.sleep(1)
    browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    browser.find_element_by_class_name('loading-more').click()
    html = etree.HTML(browser.page_source)
    duan_list=html.xpath('//div[@class="detail-wrapper"]')
    for duan in duan_list:
        print duan
        name = duan.xpath('.//img/@src')
        # name = duan.xpath('.//img/text()')

        print name




