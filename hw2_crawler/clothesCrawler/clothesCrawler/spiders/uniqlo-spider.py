import scrapy
import datetime
from clothesCrawler.items import ClothescrawlerItem


class UniqloSpider(scrapy.Spider):
    name='uniqlo'
    def start_requests(self):
        allowed_domains = ['uniqlo.com']
        urls = [
            'https://www.uniqlo.com/tw/'

        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)
        for obj in response.xpath('//*[@id="secondary"]'):
            item = ClothescrawlerItem()
            item['name'] = response.xpath('//*[@id="goodsNmArea"]/text()').extract_first()
            item['url'] = response.url
            item['obj_id'] = response.xpath('//*[@id="basic"]/li[4]/text()').extract_first()
            item['img_url'] = response.xpath('//*[@id="prodImgDefault"]/img/@src').extract_first()
            item['price'] = response.xpath('//*[@id="price"]/text()').extract_first()
            #item['store_price'] = response.xpath('//*[@id="store_price"]/text()').extract_first()
            item['colors'] = response.xpath('//*[@id="listChipColor"]/li/a/@title').extract()
            item['sizes'] = response.xpath('//*[@id="listChipSize"]/li/a/@title').extract()
            item['last_updated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if item['name'] == [] or item['name'] is None:
                continue
            yield item
        for url in response.xpath('//a/@href').extract():
            print(url)
            if url.startswith('javascript'):
                continue
            if not url.startswith('http'):
                if not url.startswith('/tw'):
                    continue
                url = 'http://www.uniqlo.com' + url

            elif url.startswith('http') :
               page = url.split('/')
               if len(page) >= 4 and page[3] is not 'tw':
                   continue

            yield scrapy.Request(response.urljoin(url))

    def __init__(self):

        from selenium import webdriver

        self.browser = webdriver.Chrome()
        super(UniqloSpider, self).__init__()

        from scrapy.xlib.pydispatch import dispatcher
        from scrapy import signals
        
        # 绑定信号量，当spider关闭时调用我们的函数
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        print('spider closed')
        #self.browser.quit()