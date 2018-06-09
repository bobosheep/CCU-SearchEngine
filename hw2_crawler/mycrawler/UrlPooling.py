import time
import lxml
import queue
import datetime
import pickle

from bs4 import BeautifulSoup
from selenium import webdriver
from scrapy.selector import Selector


def UrlPooling(cur_url, find_links, url_pool, seen_url, crawl_config):
    now_domain = cur_url.split('/')[2]
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
                if domain.find(key) >= 0:
                    if key is 'www.net-fashion.net' and linksplit[3] is 'cart':
                        break
                    pushInPool = True
                    break

            if not pushInPool : 
                continue
        else :
            #相對連結\
            if link.find('Product') >= 0 and now_domain is 'lativ.com.tw':
                #lativ.com.tw/Poduct下的資料目前不需要
                continue
            link = now_domain + link


        if link in seen_url:
            #如果url看過就略過
            continue
        
        url_pool.put(link)
        seen_url.update({link:link})
    
