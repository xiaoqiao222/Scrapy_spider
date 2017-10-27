from scrapy import cmdline
# cmdline.execute('scrapy crawl zhilians'.split())
import os
os.chdir('Zhaopin/spiders')
cmdline.execute('scrapy runspider zhilian.py'.split())