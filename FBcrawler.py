
# coding: utf-8

# In[1]:


import facebook
import json
import requests #為了要取得[next]裡面的網址z


# In[4]:


#取得FB API權杖(類似底下token)後才可以使用
#有效時間大概兩小時
#失效後就須就重新取得
token = 'EAACEdEose0cBAAB5zoZBr218OLwgSZBgn1gwW3TIjCSUPScJDdO8FZAIJZBZA5AkXqZAzlvxu3e1VphesDcolZB9bZBKLhRd7ygRGjLvoXJwBcvwEgYZAz6GYy8uAOxUjXoRH4FmfcGqEVbVhQQ43F9lJkLQgSuZC9h8AxyTUeZAg9U7Lf2yoq9eWr0QnzKVzJjvA4pdn7KAPZAkhAZDZD'
obj_fb = facebook.GraphAPI(token)


# In[21]:



kbccu_posts = obj_fb.request("haterccu",{'fields':'posts'})['posts']
print(kbccu_posts['data'][0])
#print(json.loads(requests.get(kbccu_posts['paging']['next']).text))


# In[13]:


cnt = 0
data = []
while True:
    
    for post in kbccu_posts['data']:
        if 'message' in post:
            data.append("message:"+post['message'])
            data.append("created_time:"+post['created_time'])
            data.append("id:"+post['id'])
    #print(cnt)
        cnt += 1
    print(cnt)
    if 'paging' in kbccu_posts:
        ob_post = kbccu_posts['paging']
        if 'next' in ob_post:
            kbccu_posts = json.loads(requests.get(kbccu_posts['paging']['next']).text)
        else:
            break
    else:
        break


# In[16]:


output = []
for i in data:
    s = ''
    for j in i.split('\n'):
        s += j
    output.append(s)
print(output)


# In[19]:


outF = open("OutFile.rec", "w", encoding='UTF-8')
for line in output:
  # write line to output file
      outF.write(line)
      outF.write("\n")
outF.close()

