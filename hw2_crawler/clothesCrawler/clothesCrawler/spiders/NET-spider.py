import scrapy
import datetime
from clothesCrawler.items import ClothescrawlerItem

class NetSpider(scrapy.Spider):
    name='net'
    def start_requests(self):
        allowed_domains = ['www.net-fashion.net']
        urls = [
            'https://www.net-fashion.net/'

        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)
        print('Now parse on {0}'.format(response.url))
        
        for url in response.xpath('//a/@href').extract():
            #print(url)
            if url.startswith('javascript'):
                continue
            if not url.startswith('https'):
                url = 'https://www.net-fashion.net' + url
            else:
                page = url.split('/')
            yield scrapy.Request(response.urljoin(url))

    def __init__(self):

        from selenium import webdriver

        self.browser = webdriver.Chrome()
        super(NetSpider, self).__init__()

        from scrapy.xlib.pydispatch import dispatcher
        from scrapy import signals
        
        # 绑定信号量，当spider关闭时调用我们的函数
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        print('spider closed')
        #self.browser.quit()
