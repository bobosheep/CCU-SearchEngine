# Internet Infomation Retrieval
class of Search Engine !

---

## class 2/27 

- Crawler or data gatherer //gather (v.)收集
- Data process and analysis and mining -> Data
- 工具
    - Lucene
        - 全文檢索
        - Solr
        - ElasticSearch
    - Hadoop
    - Google trend
    - Python packages
        * Requests + Beautiful soup (+ lxml for html processing)
        * scrapy 
        * [簡單易懂的入門教學](https://www.slideshare.net/tw_dsconf/python-83977397)

- Assignment 1: [ElasticSearch](https://www.elastic.co)
            - Install
            - Just design the search UI
            - No kernel required

- Search kernel & server(backend)
- Query Processor
- Service Manager

### Requirement / Prerequisite

* No textbook
* No exam
* No ~~assignment~~
* Has $$\lim_{x\to 3} f(x) $$ projects $\rightarrow$ motherfucking hard

### Assignment 1.1, Game on

* MongoDB + elastic search

MongoDB by default takes json as input data. It's noSQL, so it's pretty different from the relational database (SQL).

* Backend: use elastic search as search kernel
    * json
    * trial-and-error
    * ~~master it, and get a fucking job~~
    * [Official python elastic search package](https://github.com/elastic/elasticsearch-py)
        * 畢竟不寫kernel, python即可
* 資料: 
    * news data (will be provided)
    * 0.5 million records
* Frontend: web search UI
    * Additional features can be implemented on one's discretion
* **Deadline**: 2 weeks, 3/13 or 3/15 -> demo 
* Report
    * Code must be included
    * Written report (print it out)

總之，沒有既定的規格。要跑得起來(demo)。

[NUDB](https://github.com/vinniefalco/NuDB): source code 疑 跟吳昇說的是同一個東西嗎？ -> I doubt it...

---
## class 3/1
**各搜尋引擎比較**
*  google
*  badoo
*  bing
*  等等

### Search engine history

#### Before 1993

* started with anonymous FTP
* email, ftp, IRC, USENET
* [gopher](https://en.wikipedia.org/wiki/Gopher_(protocol))
    * 在http之前，用來檢索資料的協定
    * [Veronica](https://en.wikipedia.org/wiki/Veronica_(search_engine))
    * ![Gopher](https://blog.golang.org/gopher/header.jpg)


#### After 1993

* Web (www) emerges 
    * CERN -> 其實是粒子物理學實驗室
    * [Tim Berners-Lee WWW 制定人](https://en.wikipedia.org/wiki/Tim_Berners-Lee) 
    * proposed in 1989
    * in late 1993, mosaic

- www初期
    - mosaic -> 瀏覽器
    - Apache -> 伺服器
    - gopher -> 死去
- [Lycos](https://zh.wikipedia.org/zh-tw/Lycos)
- [Netscape](https://en.wikipedia.org/wiki/Netscape) -> Mozilla foundation -> Firefox 
- Infoseek, [Excite](http://msxml.excite.com), AltaVista (阿拉丁？）, Inktomi
- Google..., Altavista 不收購 -> thug life

**blind test** 、 **meta search**

homework 在先前一個homework一個禮拜之後

---
## class 3/6
**The course time will be changed to 13:15 ~ 14:30**
### 期末專題
* Crawler
-- *url watch*
-- *website bot* Catch a entire website
(webpage format structure, db) 
-- focused crawler/ crawler
(need general bot technique)
-- ***social media Bot***(FB / twitter) 
-- ***General web bot***
=> **UI**


#### Pseudo Code(crawler)
```
string links = "";
string pages = "";
queue<string> q;
enqueue(queue, seedurl);
while(queue not empty)
    x = dequeue(queue)
    fetcher(x, links, parser)
    newlinks = getnewlink(links)
    enqueue(queue, newlinks)
```
fetcher->geturl->parser-> news->fetcher![](https://scontent-tpe1-1.xx.fbcdn.net/v/t34.0-12/28740929_587648878255235_798258770_n.jpg?oh=1514b9b7e678274fcc7f964e606299d1&oe=5AA11F2F)

![](https://scontent-tpe1-1.xx.fbcdn.net/v/t34.0-12/28741524_587655161587940_992570908_n.jpg?oh=358fcae11267acdee6bcca0de1132d30&oe=5A9FD8FD)

### ***Important***
* parser 是取連結跟取內容
* new links 

直接抓取網站有時沒有content
需要一個 sandbox 去模擬 browser
常用PhantomJS

要把 seeDB 也記錄下來
然後可以把他打包成一個 crawling proxy


### Parser(Main content extraction)
* Main text or main block
* Represntive image 
* Content time

---
## class 3/8

![blackboard info](https://scontent-tpe1-1.xx.fbcdn.net/v/t1.0-9/28685802_1869237176421185_3874124869666865152_n.jpg?oh=2104c2fcf643ae5063c777daba54f620&oe=5B0D731D)
                  
                  
### ***page record*** 
* detag, descript
* main-tag processing
* main content extraction
	* maintext, mainblock
	* reprosentative image
	* content publish time(update time)
		* URL implication
		* content analysis (extract update time from content)
	

把parser、simulator包裝成api or proxy
beautifulsoup沒辦法給maintext

***crawling proxy:***
URL + option -> proxy -> pagerecord


