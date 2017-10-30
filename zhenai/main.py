from scrapy import cmdline
#cmdline.execute('scrapy crawl truelove'.split())
import os
os.chdir('zhenai/spiders')
cmdline.execute('scrapy runspider truelove.py'.split())