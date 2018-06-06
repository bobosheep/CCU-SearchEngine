import time
import lxml
import queue
import datetime
import pickle

from bs4 import BeautifulSoup
from selenium import webdriver
from scrapy.selector import Selector


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
            #相對連結\
            if link.find('Product') > 0 :
                #lativ.com.tw/Poduct下的資料目前不需要
                continue
            link = crawl_config['start_url'][0] + link


        if link in seen_url:
            #如果url看過就略過
            continue
        
        url_pool.put(link)
        seen_url.update({link:link})
    
