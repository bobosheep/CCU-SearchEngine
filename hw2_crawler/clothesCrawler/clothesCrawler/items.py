# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ClothescrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    obj_id = scrapy.Field()
    img_url = scrapy.Field()
    price = scrapy.Field()
    store_price = scrapy.Field()
    colors = scrapy.Field()
    sizes = scrapy.Field()
    #+ 顏色  + 評論 + size + 

    last_updated = scrapy.Field(serializer=str) 
