import requests

basepath = 'D://spiderFile/zheng800/'
# 保存标题图
frist_url = 'http://img.alicdn.com/bao/uploaded/i1/O1CN01J0iTAg1jFHw0RpfPT_!!0-rate.jpg_600x600.jpg'
fileName = basepath + frist_url[frist_url.rfind('/'):]
print(frist_url)
r = requests.get(frist_url)
with open(fileName, 'wb') as f:
    f.write(r.content)