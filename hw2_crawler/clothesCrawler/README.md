# Scrapy implementation

## Run Spider
just run a spider
```
$ scrapy crawl [spidername]

//with no item pipeline and want a outputfile
$ scrapy crawl [spidername] -o [filename]

//a spider can continue its status
$ scrapy crawl [spidername] -s JOBDIR=[dirName]
```