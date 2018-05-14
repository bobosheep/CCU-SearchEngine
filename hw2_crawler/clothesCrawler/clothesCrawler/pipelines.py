# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

class JsonPipeline(object):
    def __init__(self):
        self.Lativ = open('data/LativItems.txt', 'a+', encoding='utf8')
        self.Uniqlo = open('data/UniqloItems.json', 'w', encoding='utf8')
        self.OBdesign = open('data/OBdesignItems.json', 'w', encoding='utf8')
    def process_item(self, item, spider):
        if spider.name == 'lativ':
            for key in item :
                line = '@' + key + ':' + str(item[key]) + '\n'
                #line = json.dumps(dict(item),ensure_ascii=False) + "\n"
                self.Lativ.write(line)
            self.Lativ.write('\n')
        elif spider.name == 'uniqlo':
            line = json.dumps(dict(item),ensure_ascii=False) + "\n"
            self.Uniqlo.write(line)
        elif spider.name == 'OBdesign':
            line = json.dumps(dict(item),ensure_ascii=False) + "\n"
            self.OBdesign.write(line)
        return item
