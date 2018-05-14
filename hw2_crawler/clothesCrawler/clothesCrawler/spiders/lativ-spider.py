import scrapy
import datetime
from clothesCrawler.items import ClothescrawlerItem

visit_url = {'https://ww.latic.com.tw'}

class LativSpider(scrapy.Spider):
    name='lativ'
    global visit_url
    def start_requests(self):
        allowed_domains = ['lativ.com.tw']
        urls = [
            'https://www.lativ.com.tw'

        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)
        for obj in response.xpath('//*[@id="exhibit"]/div[2]'):
            item = ClothescrawlerItem()
            name = response.xpath('//*[@id="productImg"]/@title').extract_first()
            nameSplit = name.split('-')
            item['name'] = nameSplit[0]
            item['gender'] = nameSplit[1]
            if nameSplit[0].find('T恤') >= 0 or nameSplit[0].find('衫') >= 0 or nameSplit[0].find('衣') >= 0 \
                or nameSplit[0].find('背心') >= 0 or nameSplit[0].find('洋裝') >= 0:
                item['category'] = '衣服'
            elif nameSplit[0].find('外套') >= 0 or nameSplit[0].find('羽絨') >= 0 or nameSplit[0].find('夾克') >= 0:
                item['category'] = '外套'
            elif nameSplit[0].find('內衣') >= 0 or nameSplit[0].find('bra') >= 0 or nameSplit[0].find('細肩帶') >= 0:
                item['category'] = '內衣'
            elif nameSplit[0].find('三角褲') >= 0 or nameSplit[0].find('平口褲') >= 0 or nameSplit[0].find('安全褲') >= 0 \
                 or nameSplit[0].find('生理褲') >= 0 or nameSplit[0].find('四角褲') >= 0:
                item['category'] = '內褲'
            elif nameSplit[0].find('褲') >= 0 or nameSplit[0].find('裙') >= 0:
                item['category'] = '褲裙'
            elif nameSplit[0].find('鞋') >= 0 :
                item['category'] = '鞋'
            else :
                item['category'] = '配件'
            
            item['url'] = response.url
            item['obj_id'] = response.xpath('//*[@id="isn"]/text()').extract_first()
            item['img_url'] = response.xpath('//*[@id="productImg"]/@src').extract_first()
            if response.xpath('//*[@id="store_price"]/text()').extract_first():
                item['price'] = response.xpath('//*[@id="specialPrice"]/text()').extract_first()
                item['store_price'] = response.xpath('//*[@id="store_price"]/text()').extract_first()
            else :
                item['price'] = response.xpath('//*[@id="price"]/text()').extract_first()
            item['colors'] = response.xpath('//*[@id="exhibit"]/div[2]/div[3]/div[2]/div[3]/a/img/@title').extract()
            item['sizes'] = response.xpath('//*[@id="sizelist"]/a/text()').extract()
            item['last_updated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if item['name'] == [] or item['name'] is None:
                continue
            yield item
        for url in response.xpath('//a/@href').extract():
            #print(url)
            if url.startswith('javascript'):
                continue
            if not url.startswith('https'):
                if url.startswith('/Product'):
                    continue
                url = 'https://www.lativ.com.tw' + url
            else:
                page = url.split('/')
                if len(page) >= 4 and page[3] == 'Product' :
                    continue
            yield scrapy.Request(response.urljoin(url))

    def __init__(self):

        from selenium import webdriver

        self.browser = webdriver.Chrome()
        super(LativSpider, self).__init__()

        from scrapy.xlib.pydispatch import dispatcher
        from scrapy import signals
        
        # 绑定信号量，当spider关闭时调用我们的函数
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        print('spider closed')
        #self.browser.quit()
