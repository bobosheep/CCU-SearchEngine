import json

file = 'LativItems.txt'
cnt = 0
with open(file, "r", encoding='utf8') as fopen:
    for line in fopen:
        cnt += 1
        #print(line)
        #info = json.loads(line, encoding='utf8')
        #print(info)
    print(cnt)

    fopen.close()