import time
import lxml
import queue
import datetime
import pickle
import _thread
from threading import Thread, Lock

from bs4 import BeautifulSoup
from selenium import webdriver
from scrapy.selector import Selector

import timeit

from UrlPooling import UrlPooling
from Parser import Parser


def crawler(crawl_config, seen_url, url_pool):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')


    chrome = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=option)
    fetch_cnt = 0
    while not url_pool.empty() and fetch_cnt < crawl_config['fetch_limit']:
        #fetcher
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now)
        cur_url = url_pool.get()
        print('[{0}] {1}'.format(fetch_cnt + 1, cur_url))
        
        start = timeit.default_timer()
        
        ##use selenium
        if not cur_url.startswith('http'):
            continue
        chrome.get(cur_url)
        time.sleep(crawl_config['delay_time'])
    
        pageSource = chrome.page_source
    
        #Parser
        find_links = Parser(cur_url, pageSource, crawl_config)

        #Url Pool
        UrlPooling(cur_url, find_links, url_pool, seen_url, crawl_config)
        
        stop = timeit.default_timer()

        print("Fetch time : {0}\n".format(stop - start))
        fetch_cnt += 1

    chrome.close()
    
    crawl_end = timeit.default_timer()
    total_time = crawl_end - crawl_start
    print('Total time : {0}'.format(total_time))
    print('Average of one url time: {0}'.format(total_time / fetch_cnt))

    
        

if __name__ == "__main__":
    
    crawl_start = timeit.default_timer()

    crawl_config = {
        "delay_time" : 7,
        "threads" : 25,
        "output_dir" : "./outputdata/",
        "output_file" : "Record1.txt",
        "seenUrl_file" : "seenUrl",
        "fetch_limit" : 5000,
        "start_url":['https://www.net-fashion.net/', 'https://www.lativ.com.tw/'],
        "allow_domain": {'www.net-fashion.net':'www.net-fashion.net', 
                         'www.lativ.com.tw' : 'www.lativ.com.tw'
                        }
    }
    
    try :
        with open('stat/url_pool', 'rb') as fp:
            url_list = pickle.load(fp)
            #print(url_list)
            url_pool = queue.Queue()
            for url in url_list:
                url_pool.put(url)

        with open('stat/seen_url', 'rb') as fp:
            seen_url = pickle.load(fp)
            print(len(seen_url))
        
    except OSError :
        print('OSerror')
        url_pool = queue.Queue()
        seen_url = {}
        for url in crawl_config['start_url']:
            url_pool.put(url)
            seen_url.update({url:url})
            print(seen_url)


    threads = [Thread(target=crawler, args=(crawl_config, seen_url, url_pool,)) for i in range(crawl_config['threads'])]
    for t in threads:
        t.daemon = True
        time.sleep(10)
        t.start()
    # or [t.start() for t in threads] if you prefer the inlines

    

    # wait for threads to finish
    for t in threads:
        t.join()
    # or [t.join() for t in threads] for the inline version

    #print("main thread exited")

    
    with open('stat/url_pool', 'wb') as fp:
        pickle.dump(list(url_pool.queue), fp)
            
    with open('stat/seen_url', 'wb') as fp:
        pickle.dump(seen_url, fp)

    with open('stat/seen_url_list.txt', 'w') as fp:
        for key in seen_url:
            line = key + '\n'
            fp.write(line)
        



"""
    try:
        for i in range(crawl_config['threads']):
            _thread.start_new_thread(crawler, (crawl_config,))
            print("Create 1 thread")
    except:
        print("Error to create Thread")

        crawler(crawl_config)
"""
   
