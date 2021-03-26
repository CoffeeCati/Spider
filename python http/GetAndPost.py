import requests
# GET
GetR = requests.get('http://www.baidu.com')
print(GetR.content)

# POST
postdata = {'key': 'value'}
PostR = requests.post('http://www.xxxxxx.com/login', data=postdata)
print(PostR)
# 还有head, put, delete, options等


# URL: http://zzk.cnblogs.com/s/blogpost?Keywords=blog:qiye&pageindex=1
payload = {'Keywords': 'blog:qiye', 'pageindex': 1}
r = requests.get('http://zzk.cnblogs.com/s/blogpost', params=payload)
