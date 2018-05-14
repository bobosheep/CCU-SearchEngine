import certifi
import time
import lxml
import urllib3
import requests
import queue
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from selenium import webdriver


start_url = ['https://www.lativ.com.tw/']
allow_domain = dict({'lativ.com.tw':'lativ.com.tw'})

url_pool = dict()
urls = queue.Queue()

config = dict({
    "delay_time" : 1,
    "output_file" : "text.txt",
    
})
for url in start_url:
    urls.put(url)
    url_pool.update({url:url})
    print(url_pool)



chrome = webdriver.Chrome(executable_path='./chromedriver.exe')

#fetcher
cur_url = urls.get()
chrome.get(cur_url)
time.sleep(1)
pageSource = chrome.page_source
soup = BeautifulSoup(pageSource, 'html.parser')
result = soup.find_all('a')




