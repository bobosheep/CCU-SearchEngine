from elasticsearch import Elasticsearch
es = Elasticsearch()
#es.indices.create(index='test', ignore=400)
newsid = 1
for i in range(0, 1):
    file = '../Data/ettoday/ettoday0.rec'
    newsfile = open(file, 'r',encoding = 'utf8')
    cnt = 0
    url = ''
    title = ''
    content = ''
    news = []
    allnews = []
    print('Start!')
    print(newsfile.readline())
    print(newsfile.readline())
    print(newsfile.readline())
    print(newsfile.readline())
    print(newsfile.readline())
        json = {}
        if(cnt % 5 == 1):
            url = line
            url = url.split(':')[1] + ':' + url.split(':')[2]
            #print(url)
        elif(cnt % 5 == 2):
            title = line
            title = title.split(':')[1]
        elif(cnt % 5 == 4):
            content = line
            json = {"url":url, "title":title, "content":content}
            print(json)
            es.index(index='test', doc_type='ettoday', id = newsid, body = json)
            newsid += 1
            if(newsid % 1000 == 0):
                print('finish {} datas'.format(newsid))
        cnt += 1

    newsfile.close()

print('Finish! Total : {0}'.format(newsid))
