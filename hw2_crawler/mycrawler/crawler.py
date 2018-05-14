import certifi
import time
import lxml
import urllib3
import requests
import queue
import datetime
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from selenium import webdriver
from scrapy.selector import Selector

from lxml import etree
import timeit


start_url = ['https://www.lativ.com.tw']
allow_domain = dict({'lativ.com.tw':'lativ.com.tw'})

url_pool = dict()
urls = queue.Queue()

config = dict({
    "delay_time" : 0.2,
    "outputData_dir" : "./outputdata/",
    "output_file" : "text.txt",
    "seenUrl_file" : "seenUrl.txt", 

})
for url in start_url:
    urls.put(url)
    url_pool.update({url:url})
    print(url_pool)



chrome = webdriver.Chrome(executable_path='./chromedriver.exe')

#fetcher
while not urls.empty():
    cur_url = urls.get()
    print(cur_url)
    start = timeit.default_timer()
    chrome.get(cur_url)
    stop = timeit.default_timer()

    print("Chrome get url time : {0}".format(stop - start))

    start = timeit.default_timer()
    time.sleep(config['delay_time'])
    stop = timeit.default_timer()

    print("sleep time : {0}".format(stop - start))
    pageSource = chrome.page_source
    #print(pageSource)
    start = timeit.default_timer()
    soup = BeautifulSoup(pageSource, 'html.parser')
    stop = timeit.default_timer()

    print("beautifulSoup parse time : {0}".format(stop - start))
    
    start = timeit.default_timer()
    response = Selector(text=pageSource)
    stop = timeit.default_timer()

    print("Seletor parse time : {0}".format(stop - start))
    # extract what i want

    #parser = etree.HTMLParser()
    #response = etree.parse(soup, parser)
    #print(response.xpath('//*[@id="exhibit"]/div[2]'))
    
    for obj in response.xpath('//*[@id="exhibit"]/div[2]'):
        #print(obj)
        item = dict({
            "name":"",
            "gender":"",
            "category":"",
            "url":"",
            "obj_id":"",
            "img_url":"",
            "price":"",
            "store_price":"",
            "colors":"",
            "sizes":"",
            "last_updated":""

        })
        name = response.xpath('//*[@id="productImg"]/@title').extract_first()
        print(name)
        if name == [] or name is None:
            continue
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
        
        item['url'] = cur_url
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
        
        print(item)


    # find links
    start = timeit.default_timer()
    find_links = soup.find_all('a')
    stop = timeit.default_timer()

    print("Find all <a> parse time : {0}".format(stop - start))

    start = timeit.default_timer()
    for link in find_links:
        link = link.get('href')
        #print(link)
        if link is None or link.startswith('#') or link.startswith('javascript'):
            continue

        if link.startswith('http'):
            #check whether it is in allow_domain
            linksplit = link.split('/')
            domain = linksplit[2]
            pushInPool = False
            for key in allow_domain:
                if domain.find(key) > 0:
                    pushInPool = True
                    break
            if not pushInPool : 
                continue
        else :
            page = link.split('/')
            if len(page) >= 4 and page[3] == 'Product' :
                continue
            link = start_url[0] + link


        if link in url_pool:
            continue
        
        urls.put(link)
        url_pool.update({link:link})
    
    stop = timeit.default_timer()

    print("check url time : {0}".format(stop - start))




