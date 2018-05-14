import scrapy
import datetime
from clothesCrawler.items import ClothescrawlerItem


class OBdesignSpider(scrapy.Spider):
    name='OBdesign'
    def start_requests(self):
        allowed_domains = ['obdesign.com.tw']
        urls = [
            'https://www.obdesign.com.tw'

        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)
        for obj in response.xpath('//*[@id="product"]'):
            print("")
            item = ClothescrawlerItem()
            item['name'] = response.xpath('//*[@id="product"]/div/div[@class="name"]/text()').extract()
            item['url'] = response.url
            item['obj_id'] = response.xpath('//*[@id="product"]/div/div[@class="number"]/span[2]/text()').extract()
            item['img_url'] = response.xpath('//*[@id="product"]/div[1]/img/@src').extract()

            item['price'] = response.xpath('//*[@id="product"]/div[3]/div[5]/span[2]/text()').extract()
            #item['store_price'] = response.xpath('//*[@id="store_price"]/text()').extract()
            item['colors'] = response.xpath('//*[@id="product"]/div[3]/div[8]/div[2]/a/img/@alt').extract()
            item['sizes'] = response.xpath('//*[@id="product"]/div[3]/div[9]/div[2]/span[@data-inventory > 0]/text()').extract()
            item['last_updated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            #if item['name'] == [] or item['name'] is None:
            #    continue
            yield item
        for url in response.xpath('//a/@href').extract():
            #print(url)
            if url.startswith('javascript'):
                continue
            if not url.startswith('https'):
                url = 'https://www.obdesign.com.tw' + url

            elif url.startswith('http') :
               page = url.split('/')

            yield scrapy.Request(response.urljoin(url))

    def __init__(self):

        from selenium import webdriver

        self.browser = webdriver.Chrome()
        super(OBdesignSpider, self).__init__()

        from scrapy.xlib.pydispatch import dispatcher
        from scrapy import signals
        
        # 绑定信号量，当spider关闭时调用我们的函数
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        print('spider closed')
        #self.browser.quit()