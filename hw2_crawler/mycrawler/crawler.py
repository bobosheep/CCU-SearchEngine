import time
import lxml
import queue
import datetime
import pickle

from bs4 import BeautifulSoup
from selenium import webdriver
from scrapy.selector import Selector

from lxml import etree
import timeit







def Parser(cur_url, pageSource, crawl_config):
    soup = BeautifulSoup(pageSource, 'html.parser')
    response = Selector(text=pageSource)
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
    if cur_url.find('lativ') > 0:
        #lativ website
        for obj in response.xpath('//*[@id="exhibit"]/div[2]'):
            
            name = response.xpath('//*[@id="productImg"]/@title').extract_first()
            print(name)
            if name == [] or name is None:
                continue

            nameSplit = name.split('-')
            item['name'] = nameSplit[0]
             
            
            if item['name'] == [] or item['name'] is None:
                continue
            
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
           

            with open(crawl_config['output_dir'] + crawl_config['output_file'], "a+", encoding='utf8') as fopen:
                for key in item :
                    line = '@' + key + ':' + str(item[key]) + '\n'
                    #line = json.dumps(dict(item),ensure_ascii=False) + "\n"
                    fopen.write(line)
                fopen.write('\n')


    find_links = soup.find_all('a')
    return find_links


def UrlPooling(find_links, url_pool, seen_url, crawl_config):
    for link in find_links:
        link = link.get('href')
        #print(link)
        if link is None or link.startswith('#') or link.startswith('javascript'):
            continue

        if link.startswith('http'):
            #檢查有沒有在允許的domain裡
            linksplit = link.split('/')
            domain = linksplit[2]
            pushInPool = False

            for key in crawl_config['allow_domain']:
                if domain.find(key) > 0:
                    pushInPool = True
                    break

            if not pushInPool : 
                continue
        else :
            #相對連結
            page = link.split('/')
            if len(page) >= 2 and page[0] == 'Product' :
                #lativ.com.tw/Poduct下的資料目前不需要
                continue
            link = crawl_config['start_url'][0] + link


        if link in seen_url:
            #如果url看過就略過
            continue
        
        url_pool.put(link)
        seen_url.update({link:link})
    

def crawler(crawl_config):
            

    try :
        with open('stat/url_pool', 'rb') as fp:
            url_list = pickle.load(fp)
            url_pool = queue.Queue()
            for url in url_list:
                url_pool.put(url)

        with open('stat/seen_url', 'rb') as fp:
            seen_url = pickle.load(fp)
        
    except OSError :
        print('OSerror')
        url_pool = queue.Queue()
        seen_url = {}
        for url in crawl_config['start_url']:
            url_pool.put(url)
            seen_url.update({url:url})
            print(seen_url)


    chrome = webdriver.Chrome(executable_path='./chromedriver.exe')
    fetch_cnt = 0
    while not url_pool.empty() and fetch_cnt < crawl_config['fetch_limit']:
        #fetcher
        cur_url = url_pool.get()
        print(cur_url)
        
        start = timeit.default_timer()
        
        ##use selenium
        chrome.get(cur_url)
        time.sleep(crawl_config['delay_time'])
    
        pageSource = chrome.page_source
    
        #Parser
        find_links = Parser(cur_url, pageSource, crawl_config)

        #Url Pool
        UrlPooling(find_links, url_pool, seen_url, crawl_config)
        
        stop = timeit.default_timer()

        print("Fetch time : {0}\n".format(stop - start))
        fetch_cnt += 1

    chrome.close()

    
    with open('stat/url_pool', 'wb') as fp:
        pickle.dump(list(url_pool.queue), fp)
            
    with open('stat/seen_url', 'wb') as fp:
        pickle.dump(seen_url, fp)

    with open('stat/seen_url_list.txt', 'w') as fp:
        for key in seen_url:
            line = key + '\n'
            fp.write(line)
        

if __name__ == "__main__":
    
    crawl_config = {
        "delay_time" : 0.2,
        "threads" : 5,
        "output_dir" : "./outputdata/",
        "output_file" : "Record1.txt",
        "seenUrl_file" : "seenUrl",
        "fetch_limit" : 10000,
        "start_url":['https://www.lativ.com.tw'],
        "allow_domain": {'lativ.com.tw':'lativ.com.tw'}
    }
    


    crawler(crawl_config)

