
# coding: utf-8

# In[16]:


from elasticsearch import Elasticsearch
from elasticsearch import helpers


# In[17]:


es = Elasticsearch()
#es.indices.delete(index='facebook', ignore_unavailable=True)


# In[18]:


DOC = './data/facebook/'
BATCH_SIZE = 4000


# In[21]:


def getInfo(data):
    for line in data:
        line = line.strip()
        
        if line.startswith('message:'):
            record = dict()
            record['content'] = line[8:];
        elif line.startswith('created_time:'):
            record['created_time'] = line[13:];
        elif line.startswith('id:'):
            record['id'] = line[3:]
            record['title'] = '靠北中正-Facebook'
            record['url'] = ''
            yield record
        '''
        if line.startswith('@GAISRec:'):
            record = dict()
        elif line.startswith('@U:'):
            record['url'] = line[3:]
        elif line.startswith('@T:'):
            record['title'] = line[3:]
        elif line.startswith('@B:'):
            pass
        else:
            record['body'] = line
            yield record
        '''


# In[22]:


cnt = 0
doc1 = ['ettoday0.rec', 'ettoday1.rec', 'ettoday2.rec', 'ettoday3.rec', 'ettoday4.rec', 'ettoday5.rec']
doc2 = ['haterccu.rec']
for d in doc2:
    with open(DOC+d, "r", encoding='UTF-8') as fileopen:
         data = fileopen.readlines()
    acts = []
    for rec in getInfo(data):
        #print(rec)
        acts.append({
            '_index': 'facebook',
            '_type': 'haterccu',
            '_id': cnt,
            '_source': rec,
        })
        cnt += 1
        if len(acts) == BATCH_SIZE:
            print('finish {0} datas'.format(cnt))
            helpers.bulk(es, acts)
            acts = []
    if len(acts) > 0:
        helpers.bulk(es, acts)
        acts = []

print(cnt)
#print(data)

