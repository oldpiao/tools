import re

filepath = 'D:/job/审计公告/审计问题分词/split_words/tool_kit/词性对照表2.txt'

with open(filepath, 'r', encoding='utf-8') as f:
    data = f.read()
datas = data.split('\n')
result = []
for i in datas:
    try:
        result.append(re.search(r'(^[a-z]+) ', i).groups()[0])
    except:
        pass
print(result)
