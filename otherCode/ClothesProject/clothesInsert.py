
# coding: utf-8

# In[1]:


from elasticsearch import Elasticsearch
from elasticsearch import helpers
import time


# In[2]:


es = Elasticsearch()
lativ_DOC = '../../Data/clothes/'
BATCH_SIZE = 4000


# In[3]:

def getInfo(data):
    for line in data:
        line = line.strip()
        
        if line.startswith('@site:'):            
            record = dict()
            record['site'] = line[6:]
        elif line.startswith('@name:'):
            record['name'] = line[6:]
        elif line.startswith('@gender:'):
            record['gender'] = line[8:]
        elif line.startswith('@category:'):
            record['category'] = line[10:]
        elif line.startswith('@url:'):
            record['url'] = line[5:]
        elif line.startswith('@obj_id:'):
            record['obj_id'] = line[8:]
        elif line.startswith('@img_url:'):
            record['img_url'] = line[9:]
        elif line.startswith('@price:'):
            record['price'] = line[7:]
        elif line.startswith('@store_price:'):
            record['store_price'] = line[13:]
        elif line.startswith('@color:'):
            record['color'] = line[7:]
        elif line.startswith('@colors:'):
            record['colors'] = list()
            arr = line[8:].replace('\'', ',').replace('[', ',').replace(']', ',').split(',')
            for ele in arr :
                if len(ele) > 0 and ele != ' ' and ele != '\\xa0':
                    record['colors'].append(ele)
        elif line.startswith('@sizes:'):
            record['sizes'] = list()
            arr = line[7:].replace('\'', ',').replace('[', ',').replace(']', ',').split(',')
            for ele in arr :
                if len(ele) > 0 and ele != ' ' and ele != '\\xa0':
                    record['sizes'].append(ele)
        elif line.startswith('@last_updated:'):     
            record['last_updated'] = line[14:] 
            yield record
        
            


# In[5]:


cnt = 0

lativ_record = ['lativ_Record1.txt']

bulk_config = {
    "rec" : lativ_record,
    "doc" : lativ_DOC,
    "index" : 'clothes',    
}

batchTime = []
batchAvg = 0
batchCnt = 0
start = time.time()
for d in bulk_config['rec']:
    with open(bulk_config['doc'] + d, "r", encoding='UTF-8') as fileopen:
         data = fileopen.readlines()
    acts = []
    for rec in getInfo(data):
        #print(rec['colors'])
        #print(rec['sizes'])
        acts.append({
            '_index': bulk_config['index'],
            '_type': rec['site'],
            '_id': rec['obj_id'],
            '_source': rec,
        })
        cnt += 1
        if len(acts) == BATCH_SIZE:
            batch_start = time.time()
            print('finish {0} datas'.format(cnt))
            helpers.bulk(es, acts)
            batch_end = time.time()
            batch = batch_end - batch_start
            batchTime.append(batch)
            batchAvg += batch;
            batchCnt += 1;
            print("This batch cost {0}s".format(batch))
            
            acts = []
    if len(acts) > 0:
        helpers.bulk(es, acts)
        acts = []

end = time.time()
print(cnt)
print("total cost {0}s\nAverage batch cost {1}s\n".format((end - start), batchAvg / batchCnt))

