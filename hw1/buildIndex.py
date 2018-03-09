from elasticsearch import Elasticsearch
es = Elasticsearch()
#create index named 'test'
es.indices.create(index='test', ignore=400)

newsid = 1

for i in range(0, 6):
    #file path 
    file = 'ettoday' + str(i) + '.rec'
    newsfile = open(file, 'r',encoding = 'utf8')

    cnt = 0
    #source : {
    #   "url" : "",
    #   "title" : "",
    #   "content" : ""
    #}
    url = ''
    title = ''
    content = ''
    news = []
    allnews = []
    print('Start!')
    for line in newsfile:
        json = {}
        if(cnt % 5 == 1):
            #@U: https://.....
            url = line
            url = url.split(':')[1] + ':' + url.split(':')[2] #get URL
            #print(url)
            
        elif(cnt % 5 == 2):
            #@T: XXXX
            title = line
            title = title.split(':')[1] #get Title
            
        elif(cnt % 5 == 4):
            #get content
            content = line
            json = {"url":url, "title":title, "content":content}
            #print(json)

            #create a new document
            es.index(index='test', doc_type='ettoday', id = newsid, body = json)
            newsid += 1
            if(newsid % 1000 == 0):
                print('finish {} datas'.format(newsid))
        cnt += 1

    newsfile.close()

#finish 
print('Finish! Total : {0}'.format(newsid))
