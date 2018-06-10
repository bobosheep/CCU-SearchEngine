
import time
import lxml
import queue
import datetime
import pickle

from bs4 import BeautifulSoup
from selenium import webdriver
from scrapy.selector import Selector


def Parser(cur_url, pageSource, crawl_config):
    soup = BeautifulSoup(pageSource, 'html.parser')
    response = Selector(text=pageSource)
    item = dict()
    if cur_url.find('lativ') > 0:
        #lativ website
        item = ParseLativ(cur_url, response)
        
    #End of if cur_url.find('lativ') > 0
    if cur_url.find('net-fashion') > 0:
        # net website
        item = ParseNet(cur_url, response)
    #End of if cur_url.find('net-fashion') > 0
    if cur_url.find('50-shop') > 0:
        # 50 percent website
        item = Parse50Percent(cur_url, response)

    if item['name'] != [] and item['name'] is not None and item['name'] is not '':
            
        with open(crawl_config['output_dir'] + crawl_config['output_file'], "a+", encoding='utf8') as fopen:
            for key in item :
                line = '@' + key + ':' + str(item[key]) + '\n'
                #line = json.dumps(dict(item),ensure_ascii=False) + "\n"
                fopen.write(line)
            fopen.write('\n')
    #End of if cur_url.find('50-shop') > 0

    find_links = soup.find_all('a')
    return find_links



def ParseLativ(cur_url, response):
    
    item = dict({
                "site":"",
                "name":"",
                "gender":"",
                "category":"",
                "url":"",
                "obj_id":"",
                "img_url":"",
                "price":"",
                "store_price":"",
                "color":"",
                "colors":"",
                "sizes":"",
                "last_updated":""
            })
    for obj in response.xpath('//*[@id="exhibit"]/div[2]'):
            
            name = response.xpath('//*[@id="productImg"]/@title').extract_first()
            color = response.xpath('//span[@id="icolor"]/text()').extract_first()
            if name == [] or name is None:
                continue

            nameSplit = name.split('-')
            item['name'] = nameSplit[0]
            item['site'] = 'lativ'
            
            if item['name'] == [] or item['name'] is None:
                continue
            item['color'] = color
            print(item['name'])
            print(item['color']) 
            item['url'] = cur_url
            item['obj_id'] = response.xpath('//*[@id="isn"]/text()').extract_first()
            item['img_url'] = response.xpath('//*[@id="productImg"]/@src').extract_first() 
            item['colors'] = response.xpath('//*[@id="exhibit"]/div[2]/div[3]/div[2]/div[3]/a/img/@title').extract()
            item['sizes'] = response.xpath('//*[@id="sizelist"]/a/text()').extract()
            item['last_updated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


            if name.find('女') > 0:
                item['gender'] = '女'
            elif name.find('男') > 0:
                item['gender'] = '男'
            else :
                item['gender'] = '童'

            #衣服類
            if nameSplit[0].find('T恤') >= 0 or nameSplit[0].find('衫') >= 0 or nameSplit[0].find('衣') >= 0 \
                or nameSplit[0].find('背心') >= 0 or nameSplit[0].find('洋裝') >= 0:
                item['category'] = '衣服'
            #外套類
            elif nameSplit[0].find('外套') >= 0 or nameSplit[0].find('羽絨') >= 0 or nameSplit[0].find('夾克') >= 0:
                item['category'] = '外套'
            #內衣類
            elif nameSplit[0].find('內衣') >= 0 or nameSplit[0].find('bra') >= 0 or nameSplit[0].find('細肩帶') >= 0:
                item['category'] = '內衣'
            #內褲類
            elif nameSplit[0].find('三角褲') >= 0 or nameSplit[0].find('平口褲') >= 0 or nameSplit[0].find('安全褲') >= 0 \
                    or nameSplit[0].find('生理褲') >= 0 or nameSplit[0].find('四角褲') >= 0:
                item['category'] = '內褲'
            #褲裙類
            elif nameSplit[0].find('褲') >= 0 or nameSplit[0].find('裙') >= 0:
                item['category'] = '褲裙'
            #鞋類
            elif nameSplit[0].find('鞋') >= 0 :
                item['category'] = '鞋'
            #配件
            else :
                item['category'] = '配件'
            
            
            if response.xpath('//*[@id="store_price"]/text()').extract_first():
                #優惠價
                item['price'] = response.xpath('//*[@id="specialPrice"]/text()').extract_first()
                #原價
                item['store_price'] = response.xpath('//*[@id="store_price"]/text()').extract_first()
            else :  #可能沒有優惠價
                #價格
                item['price'] = response.xpath('//*[@id="price"]/text()').extract_first()
           

        #End for
    
    return item


def ParseNet(cur_url, response):

    
    item = dict({
                "site":"",
                "name":"",
                "gender":"",
                "category":"",
                "url":"",
                "obj_id":"",
                "img_url":"",
                "price":"",
                "store_price":"",
                "color":"",
                "colors":"",
                "sizes":"",
                "last_updated":""
            })
    for obj in response.xpath('//*[@id="main"]'):
            print('get Product')
            name = response.xpath('//*[contains(@class, "product_detail_Right_title")]/text()').extract_first()
            color = response.xpath('//*[contains(@class, "product_color_block color_active")]/div/text()').extract_first()
            if name == [] or name is None:
                continue
            name = name.split('\n')
            name = ''.join(name)
            item['name'] = name
            item['site'] = 'NET'
            
            if item['name'] == [] or item['name'] is None:
                continue
            item['color'] = color[3:]
            print(item['name'])
            print(item['color']) 
            item['url'] = cur_url
            item['obj_id'] = response.xpath('//*[contains(@class, "product_detail_Right_numberL")]/span/text()').extract_first()
            item['img_url'] = response.xpath('//*[@id="PRODUCT_IMAGE_MAIN"]/@src').extract_first() 
            colors = response.xpath('//*[contains(@class, "product_color")]/div/div/text()').extract()
            tmparr = []
            for i in colors:
                tmparr.append(i[3:])
            item['colors'] = tmparr
            item['sizes'] = response.xpath('//*[contains(@class, "product_size")]/div/a/div[contains(@class, "product_size_block")]/text()').extract()
            item['last_updated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            gender = response.xpath('//*[@id="silderbar"]/div[last()]/ul/li[last()]/ul/a/b/text()').extract_first()
            print(gender)
            if gender.find('女') != -1:
                item['gender'] = '女'
            elif gender.find('男') != -1:
                item['gender'] = '男'
            else :
                item['gender'] = '童'
            print(item['gender'])

            nameSplit = [item['name']]
            #衣服類
            if nameSplit[0].find('T') >= 0 or nameSplit[0].find('衫') >= 0 or nameSplit[0].find('衣') >= 0 \
                or nameSplit[0].find('背心') >= 0 or nameSplit[0].find('洋裝') >= 0:
                item['category'] = '衣服'
            #外套類
            elif nameSplit[0].find('外套') >= 0 or nameSplit[0].find('羽絨') >= 0 or nameSplit[0].find('夾克') >= 0:
                item['category'] = '外套'
            #內衣類
            elif nameSplit[0].find('內衣') >= 0 or nameSplit[0].find('bra') >= 0 or nameSplit[0].find('細肩帶') >= 0:
                item['category'] = '內衣'
            #內褲類
            elif nameSplit[0].find('三角褲') >= 0 or nameSplit[0].find('平口褲') >= 0 or nameSplit[0].find('安全褲') >= 0 \
                    or nameSplit[0].find('生理褲') >= 0 or nameSplit[0].find('四角褲') >= 0:
                item['category'] = '內褲'
            #褲裙類
            elif nameSplit[0].find('褲') >= 0 or nameSplit[0].find('裙') >= 0:
                item['category'] = '褲裙'
            #鞋類
            elif nameSplit[0].find('鞋') >= 0 :
                item['category'] = '鞋'
            #配件
            else :
                item['category'] = '配件'
            
            price = response.xpath('//*[contains(@class, "product_priceR_original")]/text()').extract_first()
            if price : #如果有原價的話
                #優惠價
                item['price'] = response.xpath('//*[contains(@class, "product_priceR_real")]/b/text()').extract_first()
                #原價
                price = price.split('\n')
                price = ''.join(price)
                item['store_price'] = price
            else :  #可能沒有優惠價
                #價格
                item['price'] = response.xpath('//*[contains(@class, "product_priceR_real")]/b/text()').extract_first()
           
    return item


def Parse50Percent(cur_url, response):

    item = dict({
                "site":"",
                "name":"",
                "gender":"",
                "category":"",
                "url":"",
                "obj_id":"",
                "img_url":"",
                "price":"",
                "store_price":"",
                "color":"",
                "colors":"",
                "sizes":"",
                "last_updated":""
            })

    for obj in response.xpath('//*[@id="main_content"]'):
            
            name = response.xpath('//*[@id="products_intro_content"]/p[contains(@class, "item_name")]/text()').extract_first()
            color = response.xpath('//*[@id="colors"]/a[contains(@class, "selected")]/@color').extract_first()
            if name == [] or name is None:
                continue
            name = name.split('\n')
            name = ''.join(name)
            name = name.split(' ')
            name = ''.join(name)
            item['name'] = name
            item['site'] = 'fiftypercent'
            
            if item['name'] == [] or item['name'] is None:
                continue
            item['color'] = color
            print(item['name'])
            print(item['color']) 
            item['url'] = cur_url
            id = response.xpath('//*[@id="products_intro_content"]/span[contains(@class, "item_no")]/text()').extract_first()
            item['obj_id'] = id.split(' ')[1]
            print(item['obj_id'])
            item['img_url'] = response.xpath('//*[@id="show-image"]/@src').extract_first() 
            item['colors'] = response.xpath('//*[@id="colors"]/a/@color').extract()
            item['sizes'] = response.xpath('//*[@id="sizes"]/a/text()').extract()
            item['last_updated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            check_gender = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_ucMain_navigator"]/text()').extract_first()

            if  check_gender.find('WOMEN') != -1:
                item['gender'] = '女'
            elif  check_gender.find('MEN') != -1:
                item['gender'] = '男'
            else :
                item['gender'] = '男 女'

            nameSplit = [item['name']]
            #衣服類
            if nameSplit[0].find('T恤') >= 0 or nameSplit[0].find('衫') >= 0 or nameSplit[0].find('衣') >= 0 \
                or nameSplit[0].find('背心') >= 0 or nameSplit[0].find('洋裝') >= 0:
                item['category'] = '衣服'
            #外套類
            elif nameSplit[0].find('外套') >= 0 or nameSplit[0].find('羽絨') >= 0 or nameSplit[0].find('夾克') >= 0 or nameSplit[0].find('外搭'):
                item['category'] = '外套'
            #內衣類
            elif nameSplit[0].find('內衣') >= 0 or nameSplit[0].find('bra') >= 0 or nameSplit[0].find('細肩帶') >= 0:
                item['category'] = '內衣'
            #內褲類
            elif nameSplit[0].find('三角褲') >= 0 or nameSplit[0].find('平口褲') >= 0 or nameSplit[0].find('安全褲') >= 0 \
                    or nameSplit[0].find('生理褲') >= 0 or nameSplit[0].find('四角褲') >= 0:
                item['category'] = '內褲'
            #褲裙類
            elif nameSplit[0].find('褲') >= 0 or nameSplit[0].find('裙') >= 0:
                item['category'] = '褲裙'
            #鞋類
            elif nameSplit[0].find('鞋') >= 0 :
                item['category'] = '鞋'
            #配件
            else :
                item['category'] = '配件'
            
            
            if response.xpath('//*[@id="products_intro_content"]/p[contains(@class, "item_name")]/span[contains(@class, "price")]/span/text()').extract_first():
                #優惠價
                price = response.xpath('///*[@id="products_intro_content"]/p[contains(@class, "item_name")]/span[contains(@class, "price")]/text()').extract_first()
                item['price'] = price.split('.')[1]
                #原價
                price = response.xpath('//*[@id="products_intro_content"]/p[contains(@class, "item_name")]/span[contains(@class, "price")]/span/text()').extract_first()
                item['store_price'] = price.split('.')[1]
            else :  #可能沒有優惠價
                #價格
                price = response.xpath('///*[@id="products_intro_content"]/p[1]/span[contains(@class, "price")]/text()').extract_first()
                item['price'] = price.split('.')[1]

    return item